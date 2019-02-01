from authy.api import AuthyApiClient
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
import json
import phonenumbers


class Rounds(APIView):

    def get(self, request):
        rounds = models.Round.objects.all()
        serializer = serializers.RoundSerializer(rounds, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoundsSubscribe(APIView):

    @transaction.atomic
    def post(self, request):
        is_subscribed = request.data.get('is_subscribed')
        round_id = request.data.get('round_id')

        # Check for None or ''
        if not round_id:
            return Response('round_id_missing', status=status.HTTP_400_BAD_REQUEST)

        # Validate
        if not isinstance(is_subscribed, bool):
            return Response('is_subscribed_invalid', status=status.HTTP_400_BAD_REQUEST)
        try:
            round_id_int = int(round_id)
        except ValueError:
            return Response('round_id_invalid', status=status.HTTP_400_BAD_REQUEST)

        # Find
        try:
            round = models.Round.objects.get(id=round_id_int)
        except models.Round.DoesNotExist:
            return Response('round_id_not_found', status=status.HTTP_400_BAD_REQUEST)

        old_is_subscribed = round.users.filter(id=request.user.id).exists()
        if is_subscribed and not old_is_subscribed:
            round.users.add(request.user)
            round.save()
        elif not is_subscribed and old_is_subscribed:
            round.users.remove(request.user)
            round.save()

        return Response(status=status.HTTP_200_OK)


class Self(APIView):

    def get(self, request):
        serializer = serializers.LunaUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class Responses(APIView):

    def post(self, request):
        answer_ids = request.data.get('answer_ids')

        # Validate
        if not isinstance(answer_ids, list):
            return Response('answer_ids_invalid', status=status.HTTP_400_BAD_REQUEST)

        responses = []

        try:
            with transaction.atomic():
                for answer_id in answer_ids:
                    answer_id_int = int(answer_id)
                    answer = models.SurveyAnswer.objects.get(id=answer_id_int)
                    response = models.SurveyResponse.objects.create(
                        user=request.user,
                        answer=answer,
                    )
                    responses.append(response)
        except ValueError:
            return Response('answer_ids_invalid', status=status.HTTP_400_BAD_REQUEST)
        except models.SurveyAnswer.DoesNotExist:
            return Response('answer_ids_unknown', status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response('response_duplicate', status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Questions(APIView):

    def get(self, request):
        user = request.user
        # Only include questions that haven't been answered by the user yet
        questions = models.SurveyQuestion.objects.exclude(answers__responses__user=user)
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

    @transaction.atomic
    def post(self, request):
        """
        This function accepts both anonymous and authenticated users.
        :param request:
        :return:
        """

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


class Legacy(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')

        # Success: user exists and has not been transferred
        if models.LunaUser.objects.filter(username=email).exists():
            user = models.LunaUser.objects.get(username=email)
            Token.objects.get_or_create(user=user)
            serializer = serializers.LunaUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Conflict: user has already been transferred
        elif models.LunaUser.objects.filter(email=email).exists():
            return Response('user_already_transferred', status=status.HTTP_409_CONFLICT)

        # User not found
        else:
            return Response('user_not_found', status=status.HTTP_404_NOT_FOUND)
