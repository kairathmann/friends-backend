from django.urls import reverse_lazy
from .. import models
import json
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class VerificationTokenTest(TestCaseWithAuthenticatedUser):

    def view(self):
        return 'verification_token'

    def test_post_anonymous(self):
        """
        This test is about posting to verification_token as an anonymous user.
        """
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '8000000000',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        # Get new database user
        new_user = models.LuminosUser.objects.filter(is_staff=False).exclude(id=self.user.id).get()
        self.assertEqual(response.data['id'], new_user.id)
        self.assertEqual(response.data['auth_token'], new_user.auth_token.key)
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['username'], '+498000000000')
        self.assertTrue(len(response.data['notification_id']) > 0)

    def test_post_existing(self):
        """
        This test is about posting to verification_token as an authenticated (legacy) user.
        """
        self.removeBrianBot()
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '8000000000',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.data)
        # Check existing database user
        self.assertEqual(models.LuminosUser.objects.count(), 1)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['auth_token'], self.user.auth_token.key)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['username'], '+498000000000')
        self.assertTrue(len(response.data['notification_id']) > 0)

    def test_post_400_phone_number_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '123456789',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data, 'phone_number_invalid')

    def test_post_409(self):
        """
        This test is about posting to verification_token as an authenticated user while a different user with the
        verified phone number exists.
        """
        # Create conflicting user
        models.LuminosUser.objects.create_user(
            username='+498000000000',
            first_name='conflicting_first_name',
            email='conflicting@example.com',
            password='conflicting_password')
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '8000000000',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 409, response.data)
        self.assertEqual(response.data, 'user_conflict')

    def test_exemption_positive(self):
        """
        This test checks if an exempt phone number with correct token is correctly handled.
        """
        models.PhoneVerificationExemption.objects.create(
            user=self.brianBot,
            country_code='+49',
            phone_number='15123456789',
            token='1234',
        )
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '15123456789',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.data)

    def test_exemption_negative(self):
        """
        This test checks if an exempt phone number with incorrect token is correctly handled.
        """
        models.PhoneVerificationExemption.objects.create(
            user=self.brianBot,
            country_code='+49',
            phone_number='15123456789',
            token='1234',
        )
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '15123456789',
                'country_code': '49',
                'token': '4321',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400, response.data)
