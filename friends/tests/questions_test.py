from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class QuestionsTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(QuestionsTest, self).setUp()
        self.addSurvey()

    def view(self):
        return 'questions'

    def test_get(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        # Only include questions that haven't been answered by the user yet
        self.assertIn({
            'id': self.question1.id,
            'text': self.question1.text,
            'answers': [
                {
                    'id': self.answer1b.id,
                    'text': self.answer1b.text,
                },
                {
                    'id': self.answer1a.id,
                    'text': self.answer1a.text,
                }
            ]
        }, response.data)
        self.assertNotIn({
            'id': self.question2.id,
            'text': self.question2.text,
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

    def test_filter_for_multiresponse_questions(self):
        self.addMultiResponseQuestion()

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn({
            'id': self.question1.id,
            'text': self.question1.text,
            'answers': [
                {
                    'id': self.answer1b.id,
                    'text': self.answer1b.text,
                },
                {
                    'id': self.answer1a.id,
                    'text': self.answer1a.text,
                }
            ]
        }, response.data)
        self.assertNotIn({
            'id': self.multi_response_question1.id,
            'text': self.multi_response_question1.text,
        }, response.data)
