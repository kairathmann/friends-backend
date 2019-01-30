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
        self.user.delete()


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

    def tearDown(self):
        super(TestCaseWithSurvey, self).tearDown()
        self.question1.delete()
        self.question2.delete()


class SelfResponsesTest(TestCaseWithSurvey):

    def view(self):
        return 'self_responses'

    def test_post(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_id': self.answer1a.id,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(models.SurveyResponse.objects.count(), 1)
        models.SurveyResponse.objects.all().delete()

    def test_post_401(self):
        response = self.client.post(reverse_lazy(self.view()))
        self.assertGreaterEqual(response.status_code, 400)

    def test_post_answer_id_missing(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_id': '',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_id_missing')

    def test_post_answer_id_invalid(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_id': 'invalid id',
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_id_invalid')

    def test_post_answer_id_unknown(self):
        response = self.client.post(
            reverse_lazy(self.view()),
            json.dumps({
                'answer_id': -1,
            }),
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'answer_id_unknown')


class SelfQuestionsTest(TestCaseWithSurvey):

    def view(self):
        return 'self_questions'

    def test_get(self):
        response = self.client.get(reverse_lazy(self.view()))
        self.assertEqual(response.status_code, 200)
        # Questions can be in any order but their respective answers must be sorted by order_index
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
        self.assertIn({
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
