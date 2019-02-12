from rest_framework import serializers
from . import models

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Color
        fields = [
            'id',
            'hex_value',
        ]

class LunaUserSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LunaUser, including the auth token and other private details
    '''

    emoji = serializers.SerializerMethodField('get_mock_emoji')
    def get_mock_emoji(self, user):
        return '😬' #in pycharm you don't see what's in here!

    color = ColorSerializer()

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

    color = ColorSerializer()

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

class SurveyAnsweredQuestionSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True)
    last_answer = serializers.SerializerMethodField('get_last_answer_id')

    class Meta:
        model = models.SurveyQuestion
        fields = [
            'id',
            'answers',
            'text',
            'last_answer'
        ]

    def get_last_answer_id(self, obj):
        response = models.SurveyResponse.objects\
            .filter(answer__question=obj, user_id=self.context.get('request').user.id)\
            .latest('timestamp')
        return response.answer_id

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
