from django.core.management import call_command
from ..test_case_with_authenticated_user import TestCaseWithAuthenticatedUser
from friends import models

class MakeGlobalAnnouncementTest(TestCaseWithAuthenticatedUser):

    def setUp(self):
        super(MakeGlobalAnnouncementTest, self).setUp()
        self.addMoreUsers()
        self.removeMessages()

    def test_global_announcement_success(self):
        call_command('makeglobalannouncement', 'global announcement text', '--test')

        self.assertEqual(models.Message.objects.all().count(), 3)
        for message in models.Message.objects.all():
            self.assertEqual(message.text, 'global announcement text')

    def test_global_announcement_with_placeholder(self):
        call_command('makeglobalannouncement', 'global announcement text for {user}', '--test')

        self.assertEqual(models.Message.objects.all().count(), 3)
        for message in models.Message.objects.all():
            recipient_chat_user = models.ChatUsers.objects.filter(chat=message.chat).exclude(user=message.sender).first()
            recipient = recipient_chat_user.user
            self.assertEqual(message.text, f'global announcement text for {recipient.first_name}')

    def test_global_announcement_with_empty_string(self):
        call_command('makeglobalannouncement', '', '--test')

        self.assertEqual(models.Message.objects.all().count(), 0)

    def test_global_announcement_with_no_chats(self):
        self.removeChats()

        call_command('makeglobalannouncement', 'global announcement text', '--test')

        self.assertEqual(models.Message.objects.all().count(), 0)
