from django.db import transaction
from .. import models


class ChatUtils:
    """
    Utilities for chats.
    """

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
            sender=users[0]  # TODO Remove when frontend supports system messages.
        )
        return chat
