from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Questions(APIView):

    def get(self, request):
        user = request.user
        # Only include questions that haven't been answered by the user yet
        questions = models.SurveyQuestion.objects.exclude(answers__responses__user=user)
        serializer = serializers.SurveyQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

