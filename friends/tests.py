from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from . import models
import json


class TestCaseWithAuthenticatedUser(TestCase):

    def setUp(self):
        self.user = models.LunaUser.objects.create_user(
            username='test',
            city='test-city',
            first_name='Test Name',
            email='test@example.com',
            password='test')
        self.token = Token.objects.get(user=self.user).key
        self.header = {'HTTP_AUTHORIZATION': "Bearer {}".format(self.token)}

    def tearDown(self):
        models.LunaUser.objects.all().delete()


class TestCaseWithRounds(TestCaseWithAuthenticatedUser):

    def setUp(self):
        super(TestCaseWithRounds, self).setUp()
        self.round1 = models.Round.objects.create(
            description='description1',
        )
        self.round2 = models.Round.objects.create(
            description='description2',
        )

    def tearDown(self):
        super(TestCaseWithRounds, self).tearDown()
        models.Round.objects.all().delete()


class RoundsTest(TestCaseWithRounds):

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


class RoundsSubscribeTest(TestCaseWithRounds):

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


class SelfTest(TestCaseWithAuthenticatedUser):

    def view(self):
        return 'self'

    def test_put(self):
        response = self.client.put(
            reverse_lazy(self.view()),
            json.dumps({
                'city': 'mycity',
                'first_name': 'myfirstname',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('city'), 'mycity')
        self.assertEqual(response.data.get('first_name'), 'myfirstname')

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
                'city': 'mycity',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'first_name_missing')

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

    def test_get_401(self):
        response = self.client.get(
            reverse_lazy(self.view())
        )
        self.assertEqual(response.status_code, 401)


class TestCaseWithSurvey(TestCaseWithAuthenticatedUser):

    def setUp(self):
        super(TestCaseWithSurvey, self).setUp()
        self.question1 = models.SurveyQuestion.objects.create(
            text='text1',
        )
        self.answer1a = models.SurveyAnswer.objects.create(
            question=self.question1,
            text='text1a',
            order_index=1,
        )
        self.answer1b = models.SurveyAnswer.objects.create(
            question=self.question1,
            text='text1b',
            order_index=0,
        )
        self.question2 = models.SurveyQuestion.objects.create(
            text='text2',
        )
        self.answer2a = models.SurveyAnswer.objects.create(
            question=self.question2,
            text='text2a',
            order_index=1,
        )
        self.answer2b = models.SurveyAnswer.objects.create(
            question=self.question2,
            text='text2b',
            order_index=0,
        )
        self.response2 = models.SurveyResponse.objects.create(
            user=self.user,
            answer=self.answer2a,
        )

    def tearDown(self):
        super(TestCaseWithSurvey, self).tearDown()
        models.SurveyQuestion.objects.all().delete()
        models.SurveyAnswer.objects.all().delete()
        models.SurveyResponse.objects.all().delete()


class ResponsesTest(TestCaseWithSurvey):

    def view(self):
        return 'responses'

    def test_post(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_ids': [self.answer1a.id, self.answer2b.id],
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(models.SurveyResponse.objects.count(), 3)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_post_401(self):
        response = self.client.post(reverse_lazy(self.view()))
        self.assertGreaterEqual(response.status_code, 400)

    def test_post_400_answer_ids_missing(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_ids_invalid')
        self.assertEqual(models.SurveyResponse.objects.count(), 1)

    def test_post_400_answer_ids_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_ids': ['invalid id'],
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_ids_invalid')
        self.assertEqual(models.SurveyResponse.objects.count(), 1)

    def test_post_400_second_answer_id_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_ids': [self.answer1a.id, 'invalid id', self.answer2b.id],
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_ids_invalid')
        self.assertEqual(models.SurveyResponse.objects.count(), 1)

    def test_post_400_answer_ids_unknown(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_ids': [-1],
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_ids_unknown')
        self.assertEqual(models.SurveyResponse.objects.count(), 1)


class QuestionsTest(TestCaseWithSurvey):

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


class TestCaseWithLegacy(TestCase):

    def setUp(self):
        self.legacy_user = models.LunaUser.objects.create_user(
            username='legacy@example.com')

        self.migrated_legacy_user = models.LunaUser.objects.create_user(
            username='+490123456789',
            email='migrated.legacy@example.com', )

    def tearDown(self):
        self.legacy_user.delete()
        self.migrated_legacy_user.delete()


class LegacyTest(TestCaseWithLegacy):

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
                'phone_number': '15142321157',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201, response.data)
        # Get new database user
        new_user = models.LunaUser.objects.exclude(id=self.user.id).get()
        self.assertEqual(response.data['id'], new_user.id)
        self.assertEqual(response.data['auth_token'], new_user.auth_token.key)
        self.assertEqual(response.data['city'], '')
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['username'], '+4915142321157')

    def test_post_existing(self):
        """
        This test is about posting to verification_token as an authenticated (legacy) user.
        """
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '15142321157',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.data)
        # Check existing database user
        self.assertEqual(models.LunaUser.objects.count(), 1)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['auth_token'], self.user.auth_token.key)
        self.assertEqual(response.data['city'], self.user.city)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['username'], '+4915142321157')

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
        models.LunaUser.objects.create_user(
            username='+4915142321157',
            city='conflicting_city',
            first_name='conflicting_first_name',
            email='conflicting@example.com',
            password='conflicting_password')
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'phone_number': '15142321157',
                'country_code': '49',
                'token': '1234',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 409, response.data)
        self.assertEqual(response.data, 'user_conflict')
