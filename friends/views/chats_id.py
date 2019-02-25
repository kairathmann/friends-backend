from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utilities.message_service import MessageService
from ..utilities.validation_utility import ValidationUtility
from .. import models
from .. import serializers

DEFAULT_MAX_MESSAGE_LIMIT = 15

class ChatsId(APIView):

    def get(self, request, **kwargs):
        chat_id = kwargs['id']
        user = request.user

        limit = request.GET.get('limit')
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return Response('invalid_message_limit', status=status.HTTP_400_BAD_REQUEST)
            if limit <= 0:
                return Response('invalid_message_limit', status=status.HTTP_400_BAD_REQUEST)
        else:
            limit = DEFAULT_MAX_MESSAGE_LIMIT

        from_message = request.GET.get('from_message')
        if from_message:
            try:
                from_message = int(from_message)
            except ValueError:
                return Response('invalid_from_message', status=status.HTTP_400_BAD_REQUEST)
            if from_message <= 0:
                return Response('invalid_from_message', status=status.HTTP_400_BAD_REQUEST)

        chat = get_object_or_404(models.Chat, pk=chat_id, chatusers__user=user)
        #Does the message with id from_message even belong to this chat?
        if from_message:
            try:
                chat.messages.get(pk=from_message)
            except models.Message.DoesNotExist:
                return Response('invalid_from_message', status=status.HTTP_400_BAD_REQUEST)

        # serialize chat before updating chat_unread_status in db
        serializer = serializers.ChatDetailSerializer(chat, context={'limit': limit, 'from_message': from_message})
        serializer_data = serializer.data

        # update chatusers.last_read in the db
        most_recent_message = models.Message.objects.filter(chat__exact=chat).first()
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


