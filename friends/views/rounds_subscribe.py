from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from ..utilities.validation_utility import ValidationUtility


class RoundsSubscribe(APIView):

    @transaction.atomic
    def post(self, request):
        user = request.user

        # Get round_id as int
        round_id, error_response = ValidationUtility().validate_data_object(request.data, 'round_id', int)
        if error_response:
            return error_response

        # Find round
        try:
            round = models.Round.objects.get(id=round_id)
        except models.Round.DoesNotExist:
            return Response('round_id_not_found', status=status.HTTP_400_BAD_REQUEST)

        # Get is_subscribed
        is_subscribed = request.data.get('is_subscribed')

        # Check validity of is_subscribed
        if not isinstance(is_subscribed, bool):
            return Response('is_subscribed_invalid', status=status.HTTP_400_BAD_REQUEST)

        # Check if user has answered all questions
        if is_subscribed:
            survey_questions_count = models.SurveyQuestion.objects.\
                filter(max_answers=1).\
                exclude(is_enabled=False).\
                count()
            user_responses_count = models.SurveyResponse.objects.\
                filter(user=user).\
                filter(answer__question__max_answers=1).\
                exclude(answer__question__is_enabled=False).\
                count()
            if survey_questions_count != user_responses_count:
                return Response('not_all_questions_answered', status=status.HTTP_400_BAD_REQUEST)

        old_is_subscribed = round.users.filter(id=user.id).exists()
        if is_subscribed and not old_is_subscribed:
            round.users.add(user)
            round.save()
        elif not is_subscribed and old_is_subscribed:
            round.users.remove(user)
            round.save()

        return Response(status=status.HTTP_200_OK)
