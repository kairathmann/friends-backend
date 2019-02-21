from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class QuestionsAnswered(APIView):

    def get(self, request):
        user = request.user

        questions = models.SurveyQuestion.objects

        # Only include questions that have been already answered by the user
        questions = questions.filter(answers__responses__user=user).distinct()

        # Exclude legacy questions
        questions = questions.exclude(is_enabled=False)

        # Exclude multiresponse questions
        questions = questions.filter(max_answers=1)

        # Shuffle
        questions = questions.order_by('?')

        serializer = serializers.SurveyAnsweredQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
