from django.db import transaction
from django.db.models import Count
from .. import models
from friends.utilities.user_utils import UserUtils


class ChatUtils:
    """
    Utilities for chats.
    """

    @staticmethod
    @transaction.atomic
    def create_bot_chat_creation_messages(user1, user2, message_text):
        """
        Creates messages from Brian Bot to two users that a chat between them has been created.
        No push notifications are sent for these message.
        :param user1: A user.
        :param user2: A user.
        :param message_text:
        The bot message to notify users of the new match.
        Can contain placeholders {user1} and {user2} for users\' names.
        {user1} is the user addressed by the bot, {user2} is their new match.
        :return: The two created messages.
        """
        bot_messages = []
        brian_bot = UserUtils.get_brian_bot()
        for u1, u2 in [[user1, user2], [user2, user1]]:
            chat = ChatUtils.find_chat([brian_bot, u1])
            message = models.Message.objects.create(
                chat=chat,
                text=message_text.format(user1=u1.first_name, user2=u2.first_name),
                sender=brian_bot,
            )
            bot_messages.append(message)
        return bot_messages

    @staticmethod
    @transaction.atomic
    def create_chat(users, system_message):
        """
        Creates a new chat with an initial system message. No push notifications are sent for the system message.
        :param users: A list of users.
        :param system_message: The text of the system message.
        :return: The chat.
        """
        if not isinstance(users, list):
            raise ValueError('users needs to be a list')
        if len(users) != 2:
            raise ValueError('users needs to have length 2')

        chat = models.Chat.objects.create(
            round=1,
            initial_type=models.CHAT_TYPE_FREE,
            type=models.CHAT_TYPE_FREE,
        )
        for user in users:
            models.ChatUsers.objects.create(
                chat=chat,
                user=user,
            )
        models.Message.objects.create(
            chat=chat,
            text=system_message,
            sender=None,  # system message
        )
        return chat

    @staticmethod
    def find_chat(users):
        """
        Finds the chat that contains the given users and no one else, if it exists.
        :param users: The users.
        :return: The chat, or None if it does not exists.
        """
        queryset = models.Chat.objects.annotate(num_users=Count('chatusers__user')).filter(num_users=len(users))
        for user in users:
            queryset = queryset.filter(chatusers__user=user)
        return queryset.first()
