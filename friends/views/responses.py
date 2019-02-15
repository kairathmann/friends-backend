from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models
from .. import serializers


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
