from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import models
from .. import serializers


class Chats(APIView):

    def get(self, request, **kwargs):
        user = request.user
        chats = models.Chat.objects.filter(chatusers__user=user)

        serializer = serializers.ChatOverviewSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
