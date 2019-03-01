from friends.jobs.daily.ask_for_feedback import Job
from friends import models
from ..test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class AskForFeedbackTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super().setUp()
        self.job = Job(ignore_calendar=True)

    def test_set_request_feedback(self):
        self.addMoreUsers()
        self.addChat([self.user, self.user2], round=1)
        self.addMessage()
        self.addMessage(self.user2)

        self.job.execute()

        for chatuser in models.ChatUsers.objects.filter(chat_id=self.chat1.id):
            self.assertEqual(chatuser.feedback_requested, True)

    def test_noone_talked_no_feedback(self):
        self.addMoreUsers()
        self.addChat([self.user, self.user2], round=1)
        self.job.execute()

        for chatuser in models.ChatUsers.objects.filter(chat_id=self.chat1.id):
            self.assertEqual(chatuser.feedback_requested, False)

    def test_only_one_talked_no_feedback(self):
        self.addMoreUsers()
        self.addChat([self.user, self.user2], round=1)
        self.addMessage()

        self.job.execute()

        for chatuser in models.ChatUsers.objects.filter(chat_id=self.chat1.id):
            self.assertEqual(chatuser.feedback_requested, False)

