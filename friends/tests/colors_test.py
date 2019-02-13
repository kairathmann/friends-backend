from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class ColorsTest(TestCaseWithAuthenticatedUser):

    def view(self):
        return 'colors'

    def test_get(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([
            {
                'id': 1,
                'hex_value': 'AABBCC'
            },
            {
                'id': 2,
                'hex_value': 'ABABAB'
            }
        ], response.data)

    def test_get_401(self):
        response = self.client.get(
            reverse_lazy(self.view())
        )
        self.assertEqual(response.status_code, 401)
