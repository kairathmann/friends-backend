from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers
from ..utilities.validation_utility import ValidationUtility


class Responses(APIView):

    def post(self, request):
        answer_ids, error_response = ValidationUtility().validate_data_object(request.data, "answer_ids", list)
        if error_response:
            return error_response

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

        serializer = serializers.SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
