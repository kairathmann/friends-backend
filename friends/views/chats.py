from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .. import models
from .. import serializers


class Chats(APIView):

    def get(self, request, **kwargs):
        user = request.user

        round_id = kwargs.get('round_id')

        if round_id:
            try:
                round = models.Round.objects.get(pk=round_id)
            except models.Round.DoesNotExist:
                return Response('invalid_round', status=status.HTTP_404_NOT_FOUND)

            if not round.users.filter(id=user.id).exists():
                return Response('user_not_subscribed', status=status.HTTP_404_NOT_FOUND)

            if round.start_timestamp > timezone.now():
                return Response('round_hasnt_started', status=status.HTTP_404_NOT_FOUND)

            chats = models.Chat.objects.filter(chatusers__user=user, round=round)
        else:
            chats = models.Chat.objects.filter(chatusers__user=user, round__isnull=True) | models.Chat.objects.filter(chatusers__user=user, round__end_timestamp__lte=timezone.now())

        serializer = serializers.ChatOverviewSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
