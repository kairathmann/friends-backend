from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Chat(APIView):
    def __init__(self, id):
        self.chat_id = id

    def get(self, request):
        user = request.user

        #questions = models.SurveyQuestion.objects.exclude(answers__responses__user=user)
        #serializer = serializers.ChatSerializer([], many=True)
        return Response("foo!", status=status.HTTP_200_OK)
