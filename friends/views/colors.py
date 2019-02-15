from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Colors(APIView):

    def get(self, request):
        colors = models.Color.objects.all().order_by('id')
        serializer = serializers.ColorSerializer(colors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)