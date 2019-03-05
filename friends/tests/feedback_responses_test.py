import json
from django.urls import reverse_lazy

from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser
from .. import models

class FeedbackResponsesTest(TestCaseWithAuthenticatedUser):

    def setUp(self):
        super(FeedbackResponsesTest, self).setUp()
        self.addFeedbackQuestions()
        self.addMoreUsers()
        self.removeChats()

    def view(self):
        return 'feedback_responses'

    def test_post_201(self):
        self.addChat([self.user, self.user2])

        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'feedback_responses': [
                    {
                        'feedback_question_id': self.mandatory_feedback_question1.id,
                        'rating_response': 3,
                    },
                    {
                        'feedback_question_id': self.mandatory_feedback_question2.id,
                        'rating_response': 4,
                    },
                    {
                        'feedback_question_id': self.optional_feedback_question1.id,
                        'text_response': 'feedback text response',
                    },
                ],
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), models.FeedbackResponse.objects.filter(chat_user__user__id=self.user.id).count())
        self.assertEqual(response.data[0].get('rating_response'), 3)
        self.assertEqual(response.data[1].get('rating_response'), 4)
        self.assertEqual(response.data[2].get('text_response'), 'feedback text response')

    def test_post_400_not_all_mandatory_questions_answered(self):
        self.addChat([self.user, self.user2])

        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'feedback_responses': [
                    {
                        'feedback_question_id': self.mandatory_feedback_question2.id,
                        'rating_response': 4,
                    },
                    {
                        'feedback_question_id': self.optional_feedback_question1.id,
                        'text_response': 'feedback text response',
                    },
                ],
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'not_all_mandatory_questions_answered')

    # TODO: the validators used for min/max values of rating_response aren't supported in sqlite
    # This means we can't test for e.g. 'rating_response': -1 right now
    def test_post_400_feedback_data_invalid(self):
        self.addChat([self.user, self.user2])

        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'feedback_responses': [
                    {
                        'feedback_question_id': self.mandatory_feedback_question1.id,
                        'rating_response': 3,
                    },
                    {
                        'feedback_question_id': self.mandatory_feedback_question2.id,
                        'rating_response': 6,
                    },
                    {
                        'feedback_question_id': self.optional_feedback_question1.id,
                        'text_response': 'feedback text response',
                    },
                ],
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('feedback_data_invalid', response.data)

    def test_post_404_feedback_for_chat_you_are_not_in(self):
        self.addChat([self.user2, self.user3])

        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'feedback_responses': [
                    {
                        'feedback_question_id': self.mandatory_feedback_question1.id,
                        'rating_response': 3,
                    },
                    {
                        'feedback_question_id': self.mandatory_feedback_question2.id,
                        'rating_response': 4,
                    },
                    {
                        'feedback_question_id': self.optional_feedback_question1.id,
                        'text_response': 'feedback text response',
                    },
                ],
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

