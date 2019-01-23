from rest_framework import serializers
from . import models


class LunaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LunaUser
        fields = [
            'id',
            'auth_token',
            'city',
            'first_name',
            'username',
        ]


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyAnswer
        fields = [
            'id',
            'text',
        ]


class SurveyQuestionSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True)

    class Meta:
        model = models.SurveyQuestion
        fields = [
            'id',
            'text',
            'answers',
        ]


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyResponse
        fields = [
            'id',
            'answer',
            'timestamp',
        ]
