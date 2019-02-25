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
            'emoji',
        ]


class LunaUserPartnerSerializer(serializers.ModelSerializer):
    '''
    Serialize data about a LunaUser, hiding the auth token and other private details
    '''

    color = ColorSerializer()

    class Meta:
        model = models.LunaUser
        fields = [
            'id',
            'city',
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
    user = LunaUserPartnerSerializer()

    class Meta:
        model = models.ChatUsers
        fields = [
            'user',
            'last_read',
        ]


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    def get_messages(self, chat):
        chat_messages = chat.messages

        from_message = self.context.get('from_message')
        if from_message:
            chat_messages = chat_messages.filter(id__lt=from_message)

        limit = self.context.get('limit')
        if limit:
            chat_messages = chat_messages.all()[:limit]

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


