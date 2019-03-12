from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Questions(APIView):

    def get(self, request):
        user = request.user

        questions = models.SurveyQuestion.objects

        # Only include questions that haven't been answered by the user yet
        questions = questions.exclude(answers__responses__user=user).distinct()

        # Exclude legacy questions
        questions = questions.exclude(is_enabled=False)

        # Exclude multiresponse questions
        questions = questions.filter(max_answers=1)

        questions = questions.order_by('id')

        serializer = serializers.SurveyQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
