import datetime

from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser

class ChatsTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(ChatsTest, self).setUp()
        self.addMoreUsers()

    def view(self):
        return 'chats'

    def test_get_chats_has_one_chat(self):
        self.addChat([self.user, self.user2])

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(1, len(response.data))
        self.assertEqual(2, len(response.data[0]['chatusers_set']))
        self.assertEqual('Test Name', response.data[0]['chatusers_set'][0]['user']['first_name'])
        self.assertEqual('Second', response.data[0]['chatusers_set'][1]['user']['first_name'])
        self.assertEqual('AABBCC', response.data[0]['chatusers_set'][0]['user']['color']['hex_value'])
        self.assertEqual(1, response.data[0]['chatusers_set'][0]['user']['color']['id'])
        self.assertEqual('😪', response.data[0]['chatusers_set'][0]['user']['emoji'])
        self.assertEqual('ABABAB', response.data[0]['chatusers_set'][1]['user']['color']['hex_value'])
        self.assertEqual(2, response.data[0]['chatusers_set'][1]['user']['color']['id'])
        self.assertEqual('🤠', response.data[0]['chatusers_set'][1]['user']['emoji'])

    def test_get_chats_last_message(self):
        self.addChat([self.user, self.user2])
        self.addMessage()
        self.addSecondMessage()

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]['last_message']['sender'], self.message2.sender.id)
        self.assertEqual(response.data[0]['last_message']['text'], self.message2.text)
        self.assertIsNotNone(response.data[0]['last_message']['timestamp'])

    def test_get_chats_unread_messages(self):
        self.addChat([self.user, self.user2])
        self.addMessage()
        self.addSecondMessage()

        # user1 views a specific chat (/api/v1/chats/<id>)
        self.client.get(
            reverse_lazy('chat', kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        # user1 then views all chats (/api/v1/chats/)
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        # user1's unread_messages count should be zero
        self.assertEqual(response.data[0]['unread_messages'][self.user.id], 0)
        # user2's unread_messages count should still be two
        self.assertEqual(response.data[0]['unread_messages'][self.user2.id], 2)

    def test_get_chats_has_many_chats_for_popular_users(self):
        self.addChat([self.user, self.user2])
        self.addChat([self.user, self.user3])  # SO POPULAR!

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(2, len(response.data))

    def test_no_chats_get_gets_empty_array(self):
        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(0, len(response.data))

    def test_while_others_chat_you_dont_see_them(self):
        self.addChat([self.user2, self.user3])

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(0, len(response.data))

    def test_chat_for_expired_round(self):
        self.addRounds()
        self.addChat([self.user, self.user2], self.round1)
        self.round1.users.add(self.user)
        self.round1.start_timestamp += datetime.timedelta(days=-1)
        self.round1.end_timestamp += datetime.timedelta(days=-1)
        self.round1.save()

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(1, len(response.data))

    def test_no_chat_for_current_round(self):
        self.addRounds()
        self.addChat([self.user, self.user2], self.round1)
        self.round1.users.add(self.user)
        self.round1.start_timestamp += datetime.timedelta(days=-1)
        self.round1.end_timestamp += datetime.timedelta(days=+1)
        self.round1.save()

        response = self.client.get(
            reverse_lazy(self.view()),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(0, len(response.data))
