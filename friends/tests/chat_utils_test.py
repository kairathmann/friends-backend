from .test_case_with_data import TestCaseWithData
from .. import models
from ..utilities.chat_utils import ChatUtils


class ChatUtilsTest(TestCaseWithData):

    def setUp(self):
        super(ChatUtilsTest, self).setUp()
        self.addBrianBot()
        self.addMoreUsers()
        self.removeChats()

    def test_create_chat_between_two_users(self):
        chat = ChatUtils.create_chat([self.user2, self.user3], 'Hello World!')
        self.assertEqual(models.Chat.objects.count(), 1)
        self.assertEqual(chat.chatusers_set.count(), 2)
        self.assertEqual(chat.chatusers_set.filter(user=self.user2).count(), 1)
        self.assertEqual(chat.chatusers_set.filter(user=self.user3).count(), 1)
