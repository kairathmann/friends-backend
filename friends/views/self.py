from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers
from ..utilities.validation_utility import ValidationUtility


def validate_location(location_request_data):
    required_location_keys = ['latitude', 'longitude', 'mapbox_id', 'full_name', 'name']
    return location_request_data is not None and all(
        [key in location_request_data.keys() for key in required_location_keys])


def create_location_request_entity(location_request_data, user_request_data):
    return models.Location(
        full_name=location_request_data['full_name'][:models.CITY_MAX_LENGTH],
        name=location_request_data['name'][:models.CITY_MAX_LENGTH],
        mapbox_id=location_request_data['mapbox_id'],
        latitude=location_request_data['latitude'],
        longitude=location_request_data['longitude'],
        user_id=user_request_data.id
    )


def compare_locations(location_request_entity, user_request_data):
    try:
        user_current_location = models.Location.objects.filter(user_id=user_request_data.id).latest('id')
        return location_request_entity == user_current_location
    except models.Location.DoesNotExist:
        return False


class Self(APIView):

    def get(self, request):
        serializer = serializers.LuminosUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        location = request.data.get('location')

        if validate_location(location) is False:
            return Response('city_missing', status=status.HTTP_400_BAD_REQUEST)

        first_name, error_response = ValidationUtility().validate_data_object(request.data, 'first_name', str)
        if error_response:
            return error_response
        color, error_response = ValidationUtility().validate_data_object(request.data, 'color', str)
        if error_response:
            return error_response
        emoji, error_response = ValidationUtility().validate_data_object(request.data, 'emoji', str)
        if error_response:
            return error_response

        try:
            # Get color instance from database
            color_instance = models.Color.objects.get(id=color)
        except models.Color.DoesNotExist:
            return Response('color_invalid_id', status=status.HTTP_400_BAD_REQUEST)

        # Clean
        clean_first_name = first_name[:models.FIRST_NAME_MAX_LENGTH]
        emoji_clean = emoji[:models.EMOJI_MAX_LENGTH]

        # Update
        with transaction.atomic():
            request.user.first_name = clean_first_name
            request.user.color = color_instance
            request.user.emoji = emoji_clean

            location_entity = create_location_request_entity(location, request.user)
            if compare_locations(location_entity, request.user) is False:
                location_entity.save()

            request.user.save()

        serializer = serializers.LuminosUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
