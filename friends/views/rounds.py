from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Rounds(APIView):

    def get(self, request):
        return Response(
            [
                {
                    "id": 1,
                    "start_timestamp": "2019-01-01T00:00:00Z",
                    "end_timestamp": "2019-12-31T23:59:59.999999Z",
                    "description": "",
                    "is_subscribed": True,
                }
            ], status=status.HTTP_200_OK)
