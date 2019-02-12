
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .. import models
from .. import serializers


class QuestionsAnswered(APIView):

    def get(self, request):
        user = request.user
        # Only include questions that have been already answered by the user
        questions = models.SurveyQuestion.objects.filter(answers__responses__user=user)
        serializer = serializers.SurveyAnsweredQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
