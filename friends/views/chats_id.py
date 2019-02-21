from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utilities.message_service import MessageService
from ..utilities.validation_utility import ValidationUtility
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
        MessageService(chat, user, most_recent_message).on_message_read()

        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        chat_id = kwargs['id']
        user = request.user

        text, error_response = ValidationUtility().validate_data_object(request.data, "text", str)
        if error_response:
            return error_response

        chat = get_object_or_404(models.Chat, chatusers__user=user, id__exact=chat_id)

        message = models.Message.objects.create(
            chat_id=chat_id,
            text=text,
            sender=user,
        )

        MessageService(chat, user, message).on_new_message()

        serializer = serializers.MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)


