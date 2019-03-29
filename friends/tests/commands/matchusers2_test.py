from django.core.management import call_command
from friends.tests.test_case_with_data import TestCaseWithData
from friends import models


class MatchUsers2Test(TestCaseWithData):

    def setUp(self):
        super(MatchUsers2Test, self).setUp()
        self.addBrianBot()
        self.addMoreUsers()
        self.addSurvey(None, False)
        self.addResponses(self.user2)
        self.addResponses(self.user3)

    def test_match_2_users(self):
        call_command('matchusers2', 'my-bot-message', 'my-chat-message')

        self.assertEqual(models.Chat.objects.count(), 3)
