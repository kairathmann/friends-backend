from rest_framework import serializers
from . import models


class LunaUserSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LunaUser, including the auth token and other private details
    '''

    emoji = serializers.SerializerMethodField('get_mock_emoji')
    def get_mock_emoji(self, user):
        return '😬' #in pycharm you don't see what's in here!

    color = serializers.SerializerMethodField('get_mock_color')
    def get_mock_color(self, user):
        return "{id: 1, hex_value='ca2c92'}"

    class Meta:
        model = models.LunaUser
        fields = [
            'id',
            'auth_token',
            'city',
            'first_name',
            'username',
            'color',
            'emoji'
        ]


class LunaUserPartnerSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LunaUser, hiding the auth token and other private details
    '''

    emoji = serializers.SerializerMethodField('get_mock_emoji')
    def get_mock_emoji(self, user):
        return '😬' #in pycharm you don't see what's in here!

    color = serializers.SerializerMethodField('get_mock_color')
    def get_mock_color(self, user):
        return "{id: 1, hex_value='ca2c92'}"

    class Meta:
        model = models.LunaUser
        fields = [
            'id',
            'city',
            'first_name',
            'color',
            'emoji'
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

class ChatSerializer(serializers.ModelSerializer):
    users = LunaUserPartnerSerializer(many=True)

    unread = serializers.SerializerMethodField('get_mock_unread')
    def get_mock_unread(self, chat):
        return 1

    class Meta:
        model = models.Chat
        fields = [
            'id',
            'round',
            'users',
            'type',
            'unread',
        ]
