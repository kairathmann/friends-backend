from django.urls import reverse_lazy
from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser
import json


class ChatMessageTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(ChatMessageTest, self).setUp()
        self.addMoreUsers()
        self.addChat((self.user, self.user2))

    def view(self):
        return 'chat'

    def test_chat_has_a_message(self):
        self.addMessage()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('messages')), 1)
        self.assertEqual(response.data.get('messages')[0]['text'], 'Hello World!')

    def test_chat_has_many_ordered_messages(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('messages')), 5)
        for i in range(5):
            self.assertEqual(response.data.get('messages')[i]['text'], 'Message %d'%(4-i))

    def test_unread_status_updates_after_get(self):
        self.addMessage()

        # first get request (chat_unread_status should be None)
        response1 = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response1.status_code, 200)
        self.assertIsNone(response1.data.get('chatusers_set')[0]['last_read'])

        # second get request (chat_unread_status should have been updated to self.message.id)
        response2 = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response2.status_code, 200)
        for status in response2.data.get('chatusers_set'):
            if status['user']['id'] == self.user.id:
                self.assertEqual(status['last_read'], self.message.id)

    def test_404_for_no_chat(self):
        non_existing_chat_id = 42

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": non_existing_chat_id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

    def test_404_for_not_your_chat(self):
        self.addChat((self.user2, self.user3))

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

    def test_post_400_no_text_field(self):
        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'text_field_not_found')

    def test_post_404_new_message_to_chat_you_are_not_in(self):
        self.addChat((self.user2, self.user3))

        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'text': 'Hello World!'
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 404)

    def test_post_200_new_message_sent(self):
        response = self.client.post(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            json.dumps({
                'text': 'Hello World!'
            }),
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('text'), 'Hello World!')

    def test_get_limit_to_one_newest_message(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'limit':1},
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('messages')), 1)
        self.assertEqual(response.data.get('messages')[0]['text'], 'Message 4')

    def test_get_limit_to_more_messages_than_possible_gets_whole_history(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'limit':42}, #way too many
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('messages')), 5)

    def test_get_with_limit_to_invalid_number_HTTP400(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'limit':'I am not even a number'},
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)

    def test_get_three_messages_starting_from_second_latest(self):
        messages = self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={
                'from_message': messages[4].id,
                'limit': 3
            },
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('messages')), 3)
        self.assertEqual(response.data.get('messages')[0]['text'], 'Message 3')
        self.assertEqual(response.data.get('messages')[1]['text'], 'Message 2')
        self.assertEqual(response.data.get('messages')[2]['text'], 'Message 1')

    def test_get_from_invalid_message_HTTP400(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'from_message':'I am not even a number'},
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)

    def test_get_from_unknown_message_HTTP400(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'from_message':'99999999999'},
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)

    def test_get_limit_to_negative_number_of_messages_HTTP400(self):
        self.addFiveMessages()

        response = self.client.get(
            reverse_lazy(self.view(), kwargs={"id": self.chat1.id}),
            data={'limit':-42},
            content_type='application/json',
            **self.header,
        )

        self.assertEqual(response.status_code, 400)
