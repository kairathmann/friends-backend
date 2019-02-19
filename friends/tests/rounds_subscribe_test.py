from django.urls import reverse_lazy
import json
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class RoundsSubscribeTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(RoundsSubscribeTest, self).setUp()
        self.addRounds()

    def view(self):
        return 'rounds_subscribe'

    def test_post_subscribe(self):
        # User subscribes to a round
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': True,
                'round_id': self.round1.id,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        # User is now subscribed
        self.assertEqual(self.round1.users.count(), 1)
        self.assertIn(self.user, self.round1.users.all())

    def test_post_unsubscribe(self):
        self.round1.users.add(self.user)
        # User unsubscribes from a round
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': False,
                'round_id': self.round1.id,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        # User is now unsubscribed
        self.assertEqual(self.round1.users.count(), 0)

    def test_post_400_round_id_missing(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': True,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'round_id_missing')

    def test_post_400_is_subscribed_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': 1,
                'round_id': self.round2.id,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'is_subscribed_invalid')

    def test_post_400_round_id_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': True,
                'round_id': 'a',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'round_id_invalid')

    def test_post_400_round_id_not_found(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': True,
                'round_id': -1,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'round_id_not_found')

    def test_post_401(self):
        response = self.client.post(
            reverse_lazy(self.view()),
        )
        self.assertEqual(response.status_code, 401)

    def test_post_400_not_all_questions_answered(self):
        self.addSurvey(add_responses=False)

        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'is_subscribed': True,
                'round_id': self.round1.id,
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'not_all_questions_answered')
