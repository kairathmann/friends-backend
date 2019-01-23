from authy.api import AuthyApiClient
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import get_user
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
import json
import phonenumbers


class Self(APIView):

    @transaction.atomic
    def put(self, request):
        city = request.data.get('city')
        first_name = request.data.get('first_name')

        # Check for None or ''
        if not city:
            return Response('city_missing', status=status.HTTP_400_BAD_REQUEST)
        if not first_name:
            return Response('first_name_missing', status=status.HTTP_400_BAD_REQUEST)

        # Clean
        clean_city = city[:models.CITY_MAX_LENGTH]
        clean_first_name = first_name[:models.FIRST_NAME_MAX_LENGTH]

        # Update
        request.user.city = clean_city
        request.user.first_name = clean_first_name
        request.user.save()

        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelfResponses(APIView):

    @transaction.atomic
    def post(self, request):
        json_body = request.data
        answer_id = json_body.get('answer_id')

        # Check for None or ''
        if not answer_id:
            return Response('answer_id_missing', status=status.HTTP_400_BAD_REQUEST)

        # Validate
        try:
            answer_id_int = int(answer_id)
        except:
            return Response('answer_id_invalid', status=status.HTTP_400_BAD_REQUEST)

        try:
            answer = models.SurveyAnswer.objects.get(id=answer_id_int)
        except:
            return Response('answer_id_unknown', status=status.HTTP_400_BAD_REQUEST)

        try:
            response = models.SurveyResponse.objects.create(
                user=request.user,
                answer=answer,
            )
        except:
            return Response('response_duplicate', status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.SurveyResponseSerializer(response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SelfQuestions(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        questions = models.SurveyQuestion.objects.all()
        serializer = serializers.SurveyQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


authy_api = AuthyApiClient(settings.AUTHY_ACCOUNT_SECURITY_API_KEY)


class Verification(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, request):
        phone_number = request.data.get('phone_number')
        country_code = request.data.get('country_code')
        via = request.data.get('via')

        # Check for None or ''

        if not phone_number:
            return Response('phone_number_missing', status=status.HTTP_400_BAD_REQUEST)
        if not country_code:
            return Response('country_code_missing', status=status.HTTP_400_BAD_REQUEST)
        if not via:
            return Response('via_missing', status=status.HTTP_400_BAD_REQUEST)

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


class VerificationToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        country_code = request.data.get('country_code')
        token = request.data.get('token')

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

        user, created = get_user_model().objects.get_or_create(
            username=e164,
        )
        Token.objects.get_or_create(user=user)
        serializer = serializers.LunaUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
