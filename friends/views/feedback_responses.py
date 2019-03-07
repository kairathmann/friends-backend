from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .. import serializers
from .. import models
from ..utilities.validation_utility import ValidationUtility


class FeedbackResponses(APIView):

    def post(self, request, **kwargs):
        user = request.user
        chat_id = kwargs['id']
        self.chat_user = get_object_or_404(models.ChatUsers, user=user, chat__id=chat_id)

        feedback_responses, error_response = ValidationUtility().validate_data_object(request.data, 'feedback_responses', list)
        if error_response:
            return error_response

        response_objects, error_response = self.get_response_objects_or_400(feedback_responses)

        if error_response:
            return error_response
        else:
            serializer = serializers.FeedbackResponseSerializer(response_objects, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_response_objects_or_400(self, feedback_responses):
        response_objects = []
        mandatory_questions_answered = 0

        with transaction.atomic():
            for response in feedback_responses:
                try:
                    feedback_question_id = int(response.get('feedback_question_id'))
                    feedback_question = get_object_or_404(models.FeedbackQuestion, id=feedback_question_id)

                    response_object = models.FeedbackResponse(
                        question=feedback_question,
                        chat_user=self.chat_user,
                        rating_response=response.get('rating_response'),
                        text_response=response.get('text_response'),
                    )

                    response_object.clean_fields()

                    # Increment mandatory_questions_answered tally
                    # rating_response questions are mandatory, text_response questions are not mandatory
                    if response_object.rating_response:
                        mandatory_questions_answered += 1

                    response_objects.append(response_object)
                except (ValueError, ValidationError) as e:
                    return None, Response(f'feedback_data_invalid\n{e}', status=status.HTTP_400_BAD_REQUEST)

            # Calculate total mandatory questions
            total_mandatory_questions = models.FeedbackQuestion.objects.filter(is_enabled=True, type=models.FEEDBACK_TYPE_RATING).count()
            if total_mandatory_questions != mandatory_questions_answered:
                return None, Response('not_all_mandatory_questions_answered', status=status.HTTP_400_BAD_REQUEST)

            models.FeedbackResponse.objects.bulk_create(response_objects)

            self.chat_user.feedback_requested = False
            self.chat_user.save()

        return response_objects, None

