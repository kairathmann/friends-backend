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
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'mapbox_id': '123',
                    'latitude': 1,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('latest_location').get('mapbox_id'), '123')
        self.assertEqual(response.data.get('latest_location').get('latitude'), 1)
        self.assertEqual(response.data.get('latest_location').get('longitude'), 3.14159)
        self.assertEqual(response.data.get('latest_location').get('full_name'), 'I am full name')
        self.assertEqual(response.data.get('latest_location').get('name'), 'name')
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

    def test_put_location_missing(self):
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
        self.assertEqual(response.data, 'city_missing')

    def test_put_location_latitude_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'mapbox_id': '123',
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_missing')

    def test_put_location_longitude_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'mapbox_id': '123',
                    'latitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_missing')

    def test_put_location_mapbox_id_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'latitude': 3.14159,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_missing')

    def test_put_location_full_name_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'mapbox_id': '123',
                    'latitude': 3.14159,
                    'longitude': 3.14159,
                    'name': 'name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_missing')

    def test_put_location_name_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'first_name': 'myfirstname',
                'color': 2,
                'emoji': '🤠',
                'location': {
                    'mapbox_id': '123',
                    'latitude': 3.14159,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                }
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'city_missing')

    def test_put_first_name_missing(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'location': {
                    'mapbox_id': '123',
                    'latitude': 1,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                },
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
                'location': {
                    'mapbox_id': '123',
                    'latitude': 1,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                },
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
                'location': {
                    'mapbox_id': '123',
                    'latitude': 1,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                },
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
                'location': {
                    'mapbox_id': '123',
                    'latitude': 1,
                    'longitude': 3.14159,
                    'full_name': 'I am full name',
                    'name': 'name',
                }
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
        self.assertEqual(response.data.get('first_name'), 'Test Name')
        self.assertEqual(response.data.get('color').get('id'), 1)
        self.assertEqual(response.data.get('color').get('hex_value'), 'AABBCC')
        self.assertEqual(response.data.get('emoji'), '😪')
        self.assertEqual(response.data.get('latest_location').get('latitude'), 1)
        self.assertEqual(response.data.get('latest_location').get('longitude'), 3.14159)
        self.assertEqual(response.data.get('latest_location').get('full_name'), 'I am full name')
        self.assertEqual(response.data.get('latest_location').get('mapbox_id'), '123')
        self.assertTrue(len(response.data.get('notification_id')) > 0)

    def test_get_401(self):
        response = self.client.get(
            reverse_lazy(self.view())
        )
        self.assertEqual(response.status_code, 401)
