from authy.api import AuthyApiClient
from django.conf import settings
from django.db import transaction
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import phonenumbers

from ..utilities.validation_utility import ValidationUtility


authy_api = AuthyApiClient(settings.AUTHY_ACCOUNT_SECURITY_API_KEY)


class Verification(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, request):

        phone_number, error_response = ValidationUtility().validate_data_object(request.data, 'phone_number', str)
        if error_response:
            return error_response
        country_code, error_response = ValidationUtility().validate_data_object(request.data, 'country_code', str)
        if error_response:
            return error_response
        via, error_response = ValidationUtility().validate_data_object(request.data, 'via', str)
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

        if via not in ['sms', 'call']:
            return Response('via_invalid', status=status.HTTP_400_BAD_REQUEST)

        # Authy verification
        if not settings.AUTHY_DISABLE:
            verification = authy_api.phones.verification_start(
                phone_number,
                country_code,
                via,
            )
            if not verification.ok():
                return Response('verification_failed', status=status.HTTP_400_BAD_REQUEST)

            verification_json = json.loads(verification.response.text)
            carrier = verification_json.get('carrier')[:255]
            is_cellphone = verification_json.get('is_cellphone')

        return Response(status=status.HTTP_200_OK)
