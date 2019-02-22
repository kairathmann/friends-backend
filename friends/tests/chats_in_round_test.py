from django.urls import reverse_lazy

from .test_case_with_authenticated_user import TestCaseWithAuthenticatedUser


class ChatsInRoundTest(TestCaseWithAuthenticatedUser):
    def setUp(self):
        super(ChatsInRoundTest, self).setUp()
        self.addMoreUsers()

    def view(self):
        return 'chats-for-round'

    # TODO Re-add tests when dogfooding via pairing everyone with everyone has concluded.
    # def test_round_has_chat(self):
    #     self.addChat([self.user, self.user2], 1)
    #
    #     response = self.client.get(
    #         reverse_lazy(self.view(), kwargs={'round_id': 1}),
    #         content_type='application/json',
    #         **self.header,
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['id'], self.chat1.id)
    #     self.assertEqual(response.data[0]['round'], 1)
    #
    # def test_round_has_no_chats_empty_list(self):
    #     response = self.client.get(
    #         reverse_lazy(self.view(), kwargs={'round_id': 1}),
    #         content_type='application/json',
    #         **self.header,
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data), 0)
