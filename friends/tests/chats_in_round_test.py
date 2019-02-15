import datetime

from django.urls import reverse_lazy

from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class ChatsInRoundTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(ChatsInRoundTest, self).setUp()
        self.addMoreUsers()
        self.addRounds()

    def view(self):
        return 'chats-for-round'

    def test_round_has_chat(self):
        self.round1.users.add(self.user)
        self.round1.save()
        self.addChat([self.user, self.user2], self.round1)

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': self.round1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.chat1.id)
        self.assertEqual(response.data[0]['round'], self.round1.id)

    def test_chat_in_other_round_this_round_has_no_chats(self):
        self.round1.users.add(self.user)
        self.round1.save()
        self.addChat([self.user, self.user2], self.round2)

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': self.round1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unsusbscribed_round_has_no_chats_404(self):
        self.addChat([self.user, self.user2], self.round1)

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': self.round1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

    def test_round_has_no_chats_empty_list(self):
        self.round1.users.add(self.user)
        self.round1.save()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': self.round1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_round_hasnt_started_has_no_chats_404(self):
        #move the round 1 day into the future
        self.round1.start_timestamp += datetime.timedelta(days=1)
        self.round1.end_timestamp += datetime.timedelta(days=1)
        self.round1.save()

        self.addChat([self.user, self.user2], self.round1)

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': self.round1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

    def test_round_doesnt_exist_404(self):
        response = self.client.get(
            reverse_lazy(self.view(), kwargs={'round_id': 99999999}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

