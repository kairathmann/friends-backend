from django.urls import reverse_lazy
from .. import models
import json
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class ResponsesTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(ResponsesTest, self).setUp()
        self.addSurvey()

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
        self.assertEqual(models.SurveyResponse.objects.count(), 4)
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
        self.assertEqual(models.SurveyResponse.objects.count(), 2)

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
        self.assertEqual(models.SurveyResponse.objects.count(), 2)

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
        self.assertEqual(models.SurveyResponse.objects.count(), 2)

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
        self.assertEqual(models.SurveyResponse.objects.count(), 2)
