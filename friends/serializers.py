from rest_framework import serializers
from . import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = [
            'id',
            'hex_value',
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = [
            'id',
            'mapbox_id',
            'name',
            'full_name',
            'latitude',
            'longitude',
        ]


class LuminosUserSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LuminosUser, including the auth token and other private details
    '''

    color = ColorSerializer()
    latest_location = serializers.SerializerMethodField()
    def get_latest_location(self, user):
        latest = models.Location.objects.filter(user=user).last()
        return LocationSerializer(latest).data


    def to_representation(self, obj):
        ret = super(LuminosUserSerializer, self).to_representation(obj)

        if ret['latest_location'] is None:
            del ret['latest_location']
        return ret



    class Meta:
        model = models.LuminosUser
        fields = [
            'id',
            'auth_token',
            'first_name',
            'username',
            'color',
            'emoji',
            'latest_location',
            'notification_id'
        ]


class LuminosUserPartnerSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LuminosUser, hiding the auth token and other private details
    '''

    color = ColorSerializer()

    class Meta:
        model = models.LuminosUser
        fields = [
            'id',
            'first_name',
            'color',
            'emoji',
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
        response = models.SurveyResponse.objects \
            .filter(answer__question=obj, user_id=self.context.get('user').id) \
            .last()
        return response.answer_id


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyResponse
        fields = [
            'id',
            'answer',
            'timestamp',
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = [
            'id',
            'sender',
            'timestamp',
            'text'
        ]


class ChatUsersSerializer(serializers.ModelSerializer):
    user = LuminosUserPartnerSerializer()

    class Meta:
        model = models.ChatUsers
        fields = [
            'user',
            'last_read',
            'feedback_requested'
        ]


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    def get_messages(self, chat):
        chat_messages = chat.messages

        from_message = self.context.get('from_message')
        if from_message:
            chat_messages = chat_messages.filter(id__lt=from_message)

        until_message = self.context.get('until_message')
        if until_message:
            chat_messages = chat_messages.filter(id__gt=until_message)

        chat_messages = chat_messages.reverse()
        limit = self.context.get('limit')
        if limit and not until_message: # until_message overrides limit
            if chat_messages.count() > limit:
                chat_messages = chat_messages.all()[chat_messages.count()-limit:]

        return MessageSerializer(chat_messages, many=True).data

    chatusers_set = ChatUsersSerializer(many=True)

    class Meta:
        model = models.Chat
        fields = [
            'id',
            'round',
            'type',
            'chatusers_set',
            'messages'
        ]


class ChatOverviewSerializer(serializers.ModelSerializer):
    chatusers_set = ChatUsersSerializer(many=True)

    last_message = serializers.SerializerMethodField()
    def get_last_message(self, chat):
        return MessageSerializer(chat.messages.first()).data

    unread_messages = serializers.SerializerMethodField()
    def get_unread_messages(self, chat):
        unread_messages_dict = {}

        for chatuser in chat.chatusers_set.all():
          if chatuser.last_read == None:
            unread_messages_dict[chatuser.user.id] = chatuser.chat.messages.all().count()
          else:
            unread_messages_dict[chatuser.user.id] = chatuser.chat.messages.filter(id__gt=chatuser.last_read.id).count()

        return unread_messages_dict

    class Meta:
        model = models.Chat
        fields = [
            'id',
            'round',
            'type',
            'chatusers_set',
            'last_message',
            'unread_messages',
        ]


class FeedbackQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FeedbackQuestion
        fields = [
            'id',
            'text',
            'order_index',
            'type',
        ]


class FeedbackResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FeedbackResponse
        fields = [
            'question',
            'chat_user',
            'rating_response',
            'text_response',
        ]
