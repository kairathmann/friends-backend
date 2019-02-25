from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class QuestionsAnsweredTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(QuestionsAnsweredTest, self).setUp()
        self.addSurvey()

    def view(self):
        return 'questions_answered'

    def test_get(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn({
            'id': self.question2.id,
            'text': self.question2.text,
            'last_answer': self.response2b.answer.id,
            'answers': [
                {
                    'id': self.answer2b.id,
                    'text': self.answer2b.text,
                },
                {
                    'id': self.answer2a.id,
                    'text': self.answer2a.text,
                }
            ]
        }, response.data)
