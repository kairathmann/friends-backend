from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from friends import models
from friends.utilities.chat_utils import ChatUtils
from friends.utilities.message_service import MessageService
from friends.utilities.user_utils import UserUtils


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'bot-message',
            help='The bot message to notify users of the new match. '
                 'Can contain placeholders {user1} and {user2} for users\' names. '
                 '{user1} is the user addressed by the bot, {user2} is their new match.',
        )
        parser.add_argument(
            'chat-message',
            help='The system message to appear in the chats between matched users. '
                 'Can contain {user1} and {user2} for users\' names. '
                 'Assume {user1} and {user2} are interchangeable.',
        )

    def handle(self, *args, **options):
        """
        The 'matchusers' custom command tries to create one new 2-person chat for every user.
        :param args: bot-message, chat-message.
        :param options: None.
        :return: Nothing.
        """

        # We pair the users with the most number of existing chats first because they have the fewest options.

        # A list of all users in descending order of existing chats.
        user_list = list(UserUtils.exclude_brian_bot().annotate(num_chats=Count('chatusers')).order_by('-num_chats'))

        # paired_list[i] contains the user that user_list[i] has been paired with.
        paired_list = [None for _ in range(len(user_list))]

        # Brian-Bot messages to participants.
        bot_messages = []

        with transaction.atomic():
            for i in range(len(user_list)):
                if not paired_list[i]:
                    user1 = user_list[i]
                    for j in range(i + 1, len(user_list)):
                        user2 = user_list[j]
                        if not paired_list[j] and not ChatUtils.find_chat([user1, user2]):
                            ChatUtils.create_chat(
                                [user1, user2],
                                options['chat-message'].format(user1=user1.first_name, user2=user2.first_name)
                            )
                            self.stdout.write('Pairing user {} and user {}.'.format(user1.first_name, user2.first_name))
                            paired_list[i] = user2
                            paired_list[j] = user1
                            # Create Brian-Bot message to participants.
                            bot_messages.extend(
                                ChatUtils.create_bot_chat_creation_messages(user1, user2, options['bot-message']))
                            # Stop looking for further matches for user i.
                            break

        for i in range(len(user_list)):
            if not paired_list[i]:
                self.stdout.write('User {} not paired.'.format(user_list[i].first_name))

        # Send push notifications for messages.
        brian_bot = UserUtils.get_brian_bot()
        for message in bot_messages:
            try:
                MessageService(message.chat, brian_bot, message).on_new_message()
            except:
                pass
