from django.urls import reverse_lazy
import json
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class SelfTest(TestCaseWithAuthenticatedUser):

    def view(self):
        return 'self'

    def test_put(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'city': 'mycity',
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('city'), 'mycity')
        self.assertEqual(response.data.get('first_name'), 'myfirstname')
        self.assertEqual(response.data.get('color').get('id'), 2)
        self.assertEqual(response.data.get('color').get('hex_value'), 'ABABAB')
        self.assertEqual(response.data.get('emoji'), '🤠')
        self.assertTrue(len(response.data.get('notification_id')) > 0)

    def test_put_401(self):
        response = self.client.put(
            reverse_lazy(self.view())
        )
        self.assertEqual(response.status_code, 401)

    def test_put_city_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠'
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_field_not_found')

    def test_put_first_name_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'city': 'mycity',
                'color': 2,
                'emoji': '🤠'
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'first_name_field_not_found')

    def test_put_color_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'city': 'mycity',
                'first_name': 'myfirstname',
                'emoji': '🤠'
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'color_field_not_found')

    def test_put_color_invalid_id(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'city': 'mycity',
                'first_name': 'myfirstname',
                'color': 10,
                'emoji': '🤠'
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'color_invalid_id')

    def test_put_emoji_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'city': 'mycity'
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'emoji_field_not_found')

    def test_get(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('username'), 'test')
        self.assertEqual(response.data.get('city'), 'test-city')
        self.assertEqual(response.data.get('first_name'), 'Test Name')
        self.assertEqual(response.data.get('color').get('id'), 1)
        self.assertEqual(response.data.get('color').get('hex_value'), 'AABBCC')
        self.assertEqual(response.data.get('emoji'), '😪')
        self.assertTrue(len(response.data.get('notification_id')) > 0)

    def test_get_401(self):
        response = self.client.get(
            reverse_lazy(self.view())
        )
        self.assertEqual(response.status_code, 401)
