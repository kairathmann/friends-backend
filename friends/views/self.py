from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


class Self(APIView):

    def get(self, request):
        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        city = request.data.get('city')
        first_name = request.data.get('first_name')
        color = request.data.get('color')

        # Check for None or ''
        if not city:
            return Response('city_missing', status=status.HTTP_400_BAD_REQUEST)
        if not first_name:
            return Response('first_name_missing', status=status.HTTP_400_BAD_REQUEST)
        if not color:
            return Response('color_missing', status=status.HTTP_400_BAD_REQUEST)

        color_instance = None
        try:
            # Get color instance from database
            color_instance = models.Color.objects.get(id=color)
        except models.Color.DoesNotExist:
            return Response('color_invalid_id', status=status.HTTP_400_BAD_REQUEST)

        # Clean
        clean_city = city[:models.CITY_MAX_LENGTH]
        clean_first_name = first_name[:models.FIRST_NAME_MAX_LENGTH]

        # Update
        request.user.city = clean_city
        request.user.first_name = clean_first_name
        request.user.color = color_instance
        request.user.save()

        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
