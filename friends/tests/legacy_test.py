from django.urls import reverse_lazy
import json
from .test_case_with_data import TestCaseWithData


class LegacyTest(TestCaseWithData):
    def setUp(self):
        super(LegacyTest, self).setUp()
        self.addLegacyUsers()

    def view(self):
        return 'legacy'

    def test_post_201(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'email': self.legacy_user.username,
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('username'), 'legacy@example.com')

    def test_post_user_already_transferred(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'email': self.migrated_legacy_user.email,
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data, 'user_already_transferred')

    def test_post_user_not_found(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'email': 'non.legacy.email@example.com',
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'user_not_found')
