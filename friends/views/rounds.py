from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Rounds(APIView):

    def get(self, request):
        rounds = models.Round.objects.all()
        serializer = serializers.RoundSerializer(rounds, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
