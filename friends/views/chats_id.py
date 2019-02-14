from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class ChatsId(APIView):

    def get(self, request, **kwargs):
        chat_id = kwargs['id']
        user = request.user
        chat = get_object_or_404(models.Chat, pk=chat_id, chatusers__user=user)

        # serialize chat before updating chat_unread_status in db
        serializer = serializers.ChatDetailSerializer(chat)
        serializer_data = serializer.data

        # update chatusers.last_read in the db
        most_recent_message = models.Message.objects.filter(chat__exact=chat).last()
        self.update_last_read(chat, user, most_recent_message)

        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        chat_id = kwargs['id']
        user = request.user
        chat = get_object_or_404(models.Chat, chatusers__user=user, id__exact=chat_id)
        text = request.data.get('text')

        if not text:
          return Response('no_text_field', status=status.HTTP_400_BAD_REQUEST)

        message = models.Message.objects.create (
            chat_id=chat_id,
            text=text,
            sender=user,
          )

        # update chatusers.last_read in the db
        self.update_last_read(chat, user, message)

        serializer = serializers.MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_last_read(self, chat, user, message):
        chat_user = chat.chatusers_set.get(user=user)
        chat_user.last_read = message
        chat_user.save()




