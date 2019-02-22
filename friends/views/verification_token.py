import phonenumbers
from authy.api import AuthyApiClient
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import serializers
from ..utilities.validation_utility import ValidationUtility


authy_api = AuthyApiClient(settings.AUTHY_ACCOUNT_SECURITY_API_KEY)


class VerificationToken(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, request):
        """
        This function accepts both anonymous and authenticated users.
        :param request:
        :return:
        """

        phone_number, error_response = ValidationUtility().validate_data_object(request.data, 'phone_number', str)
        if error_response:
            return error_response
        country_code, error_response = ValidationUtility().validate_data_object(request.data, 'country_code', str)
        if error_response:
            return error_response
        token, error_response = ValidationUtility().validate_data_object(request.data, 'token', str)
        if error_response:
            return error_response

        # Validate
        if not country_code.startswith('+'):
            country_code = '+' + country_code

        full_phone_number = country_code + phone_number
        try:
            full_phone_number_object = phonenumbers.parse(full_phone_number)
            if not phonenumbers.is_valid_number(full_phone_number_object):
                return Response('phone_number_invalid', status=status.HTTP_400_BAD_REQUEST)
            e164 = phonenumbers.format_number(full_phone_number_object, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            return Response('phone_number_invalid', status=status.HTTP_400_BAD_REQUEST)

        # Authy verification
        if not settings.AUTHY_DISABLE:
            verification = authy_api.phones.verification_check(
                phone_number,
                country_code,
                token,
            )
            if not verification.ok():
                return Response('verification_failed', status=status.HTTP_400_BAD_REQUEST)

        if request.user.id is None:
            user, created = get_user_model().objects.get_or_create(
                username=e164,
            )
            Token.objects.get_or_create(user=user)
        else:
            if get_user_model().objects.filter(username=e164).exists():
                return Response('user_conflict', status=status.HTTP_409_CONFLICT)
            request.user.username = e164
            request.user.save()
            user = request.user

        serializer = serializers.LunaUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

