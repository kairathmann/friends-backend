from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class RoundsTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(RoundsTest, self).setUp()
        self.addRounds()

    def view(self):
        return 'rounds'

    def test_get_2_unsubscribed(self):
        # Two existing rounds, user not subscribed
        response = self.client.get(
            reverse_lazy(self.view()),
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue([x for x in response.data if (
            x['id'] == self.round1.id and
            x['description'] == self.round1.description and
            not x['is_subscribed']
        )])
        self.assertTrue([x for x in response.data if (
            x['id'] == self.round2.id and
            x['description'] == self.round2.description and
            not x['is_subscribed']
        )])

    def test_get_1_subscribed(self):
        self.round1.users.add(self.user)
        # User is now subscribed
        response = self.client.get(
            reverse_lazy(self.view()),
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue([x for x in response.data if (
            x['id'] == self.round1.id and
            x['description'] == self.round1.description and
            x['is_subscribed']
        )])
        self.assertTrue([x for x in response.data if (
            x['id'] == self.round2.id and
            x['description'] == self.round2.description and
            not x['is_subscribed']
        )])

    def test_get_401(self):
        response = self.client.get(
            reverse_lazy(self.view()),
        )
        self.assertEqual(response.status_code, 401)
