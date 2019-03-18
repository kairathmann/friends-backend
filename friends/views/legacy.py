from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers
from ..utilities.validation_utility import ValidationUtility


class Legacy(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email, error_response = ValidationUtility().validate_data_object(request.data, "email", str)
        if error_response:
            return error_response

        # Success: user exists and has not been transferred
        if models.LuminosUser.objects.filter(username=email).exists():
            user = models.LuminosUser.objects.get(username=email)
            Token.objects.get_or_create(user=user)
            serializer = serializers.LuminosUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Conflict: user has already been transferred
        elif models.LuminosUser.objects.filter(email=email).exists():
            return Response('user_already_transferred', status=status.HTTP_409_CONFLICT)

        # User not found
        else:
            return Response('user_not_found', status=status.HTTP_404_NOT_FOUND)
