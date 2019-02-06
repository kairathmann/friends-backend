from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Chats(APIView):

    def get(self, request):
        user = request.user

        chats = models.Chat.objects.filter(users__in=[user])
        serializer = serializers.ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
