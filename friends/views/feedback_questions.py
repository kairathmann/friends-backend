from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .. import serializers
from .. import models


class FeedbackQuestions(APIView):

    def get(self, request):
        feedback_questions = models.FeedbackQuestion.objects.filter(is_enabled=True)
        serializer = serializers.FeedbackQuestionSerializer(feedback_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
