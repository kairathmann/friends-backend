import json
from django.urls import reverse_lazy

from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class FeedbackQuestionsTest(TestCaseWithAuthenticatedUser):

    def setUp(self):
        super(FeedbackQuestionsTest, self).setUp()
        self.addFeedbackQuestions()

    def view(self):
        return 'feedback_questions'

    def test_get_feedback_questions_200(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get('text'), self.mandatory_feedback_question1.text)
        self.assertEqual(response.data[1].get('text'), self.mandatory_feedback_question2.text)
        self.assertEqual(response.data[2].get('text'), self.optional_feedback_question1.text)

    def test_get_feedback_questions_401(self):
        response = self.client.get(
            reverse_lazy(self.view())
        )

        self.assertEqual(response.status_code, 401)
