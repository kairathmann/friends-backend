from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers
from ..utilities.validation_utility import ValidationUtility


class Self(APIView):

    def get(self, request):
        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        city, error_response = ValidationUtility().validate_data_object(request.data, 'city', str)
        if error_response:
            return error_response
        first_name, error_response = ValidationUtility().validate_data_object(request.data, 'first_name', str)
        if error_response:
            return error_response
        color, error_response = ValidationUtility().validate_data_object(request.data, 'color', str)
        if error_response:
            return error_response
        emoji, error_response = ValidationUtility().validate_data_object(request.data, 'emoji', str)
        if error_response:
            return error_response

        color_instance = None
        try:
            # Get color instance from database
            color_instance = models.Color.objects.get(id=color)
        except models.Color.DoesNotExist:
            return Response('color_invalid_id', status=status.HTTP_400_BAD_REQUEST)

        # Clean
        clean_city = city[:models.CITY_MAX_LENGTH]
        clean_first_name = first_name[:models.FIRST_NAME_MAX_LENGTH]
        emoji_clean = emoji[:models.EMOJI_MAX_LENGTH]

        # Update
        with transaction.atomic():
            request.user.city = clean_city
            request.user.first_name = clean_first_name
            request.user.color = color_instance
            request.user.emoji = emoji_clean
            request.user.save()

        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
