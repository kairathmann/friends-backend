from django.core.management import call_command
from friends.tests.test_case_with_data import TestCaseWithData
from friends.models import Chat
from friends.models import ChatUsers
from friends.models import CHAT_TYPE_FREE
from friends.models import Message
from friends.utilities.chat_utils import ChatUtils


class MatchUsersTest(TestCaseWithData):

    def setUp(self):
        super(MatchUsersTest, self).setUp()
        self.addLuminosBot()
        self.addMoreUsers()

    def test_match_2_unmatched_users(self):
        # Tests the creation of chats and messages.

        self.assertFalse(Chat.objects.filter(chatusers__user=self.user2).filter(chatusers__user=self.user3).exists())
        call_command('matchusers', 'my-bot-message {user1} {user2}', 'my-chat-message {user1} {user2}')

        # Messages are ordered by -id, hence the first message is the newest.

        user2_user3_chat = ChatUtils.find_chat([self.user2, self.user3])
        user2_user3_message = user2_user3_chat.messages.first()
        self.assertEqual(user2_user3_message.sender, None)
        self.assertEqual(user2_user3_message.text, 'my-chat-message {} {}'.format(
            self.user2.first_name, self.user3.first_name
        ))

        bot_user2_chat = ChatUtils.find_chat([self.luminosBot, self.user2])
        bot_user2_message = bot_user2_chat.messages.first()
        self.assertEqual(bot_user2_message.sender, self.luminosBot)
        self.assertEqual(bot_user2_message.text, 'my-bot-message {} {}'.format(
            self.user2.first_name, self.user3.first_name
        ))

        bot_user3_chat = ChatUtils.find_chat([self.luminosBot, self.user3])
        bot_user3_message = bot_user3_chat.messages.first()
        self.assertEqual(bot_user3_message.sender, self.luminosBot)
        self.assertEqual(bot_user3_message.text, 'my-bot-message {} {}'.format(
            self.user3.first_name, self.user2.first_name
        ))

    def test_match_3_unmatched_users(self):
        # Tests that 3 unmatched users results in just 1 new chat.

        self.addAuthenticatedUser()
        num_chats = Chat.objects.count()
        call_command('matchusers', 'my-bot-message {user1} {user2}', 'my-chat-message {user1} {user2}')
        self.assertEqual(Chat.objects.count(), num_chats + 1)

    def test_dont_match_matched_users(self):
        chat = Chat.objects.create(initial_type=CHAT_TYPE_FREE, type=CHAT_TYPE_FREE)
        ChatUsers.objects.create(chat=chat, user=self.user2)
        ChatUsers.objects.create(chat=chat, user=self.user3)
        num_chats = Chat.objects.count()
        num_messages = Message.objects.count()
        call_command('matchusers', 'my-bot-message', 'my-chat-message')
        self.assertEqual(Chat.objects.count(), num_chats)
        self.assertEqual(Message.objects.count(), num_messages)
