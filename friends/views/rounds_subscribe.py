from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RoundsSubscribe(APIView):

    @transaction.atomic
    def post(self, request):
        return Response(status=status.HTTP_200_OK)
