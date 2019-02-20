from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models


class RoundsSubscribe(APIView):

    @transaction.atomic
    def post(self, request):
        is_subscribed = request.data.get('is_subscribed')
        round_id = request.data.get('round_id')
        user = request.user

        # Check if user has answered all questions
        if is_subscribed:
            survey_questions_count = models.SurveyQuestion.objects.filter(max_answers=1).count()
            user_responses_count = models.SurveyResponse.objects.filter(user=user).count()
            if survey_questions_count != user_responses_count:
                return Response('not_all_questions_answered', status=status.HTTP_400_BAD_REQUEST)

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

        old_is_subscribed = round.users.filter(id=user.id).exists()
        if is_subscribed and not old_is_subscribed:
            round.users.add(user)
            round.save()
        elif not is_subscribed and old_is_subscribed:
            round.users.remove(user)
            round.save()

        return Response(status=status.HTTP_200_OK)
