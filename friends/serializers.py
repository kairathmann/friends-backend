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


class RoundSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = models.Round
        fields = [
            'id',
            'start_timestamp',
            'end_timestamp',
            'description',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        """
        Getter for the custom field 'is_subscribed'.
        :param obj: The Round object.
        :return: The contents of the custom field 'is_subscribed'.
        """
        return obj.users.filter(id=self.context.get('request').user.id).exists()
