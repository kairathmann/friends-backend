from django.core.management.base import BaseCommand
from friends import models
from friends.utilities.chat_utils import ChatUtils
from friends.utilities.message_service import MessageService
from friends.utilities.user_utils import UserUtils



class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout=stdout, stderr=stderr, no_color=no_color)

        self.user_list = list(UserUtils.exclude_brian_bot())

        self.question_count = models.SurveyQuestion.objects\
            .distinct()\
            .exclude(is_enabled=False)\
            .filter(max_answers=1)\
            .count()

        self.user_responses = {u: models.SurveyResponse.objects.filter(user=u) for u in self.user_list}

        self.s_scores = {}

    def add_arguments(self, parser):
        parser.add_argument(
            'bot-message',
            help='The bot message to notify users of the new match. '
                 'Can contain placeholders {user1} and {user2} for users\' names. '
                 '{user1} is the user addressed by the bot, {user2} is their new match.',
        )
        parser.add_argument(
            'chat-message',
            help='The system message to appear in the chats between matched users. '
                 'Can contain {user1} and {user2} for users\' names. '
                 'Assume {user1} and {user2} are interchangeable.',
        )

    def s_score(self, user_a, user_b):
        responses_a = set(r.answer for r in self.user_responses[user_a][::1])
        responses_b = set(r.answer for r in self.user_responses[user_b][::1])

        return len(responses_a.intersection(responses_b)) / self.question_count


    def max_score(self, user):
        return max(self.s_scores[user].values())

    def handle(self, *args, **options):
        """
        The 'matchusers2' custom command tries to create one new 2-person chat for every user.
        :param args: bot-message, chat-message.
        :param options: None.
        :return: Nothing.
        """

        # Brian-Bot messages to participants.
        bot_messages = []

        self.s_scores = {i:{j:0.0 for j in self.user_list} for i in self.user_list}

        for i in range(len(self.user_list)):
            for j in range(i):
                score = self.s_score(self.user_list[i], self.user_list[j])
                self.s_scores[self.user_list[i]][self.user_list[j]] = score
                self.s_scores[self.user_list[j]][self.user_list[i]] = score

        match_candidates = list(self.user_list)

        while True:
            match_candidates.sort(key=self.max_score)

            user1 = match_candidates[-1]
            max_score = self.max_score(user1)
            if max_score < 0.5:
                break

            user2 = None
            for u in self.user_list:
                if self.s_scores[user1][u] == max_score:
                    user2 = u

            ChatUtils.create_chat(
                [user1, user2],
                options['chat-message'].format(user1=user1.first_name, user2=user2.first_name)
            )
            self.stdout.write('Pairing user {} and user {}.'.format(user1.first_name, user2.first_name))

            for u in self.user_list:
                self.s_scores[u][user1] = 0.0
                self.s_scores[u][user2] = 0.0
                self.s_scores[user1][u] = 0.0
                self.s_scores[user2][u] = 0.0

            # Create Brian-Bot message to participants.
            bot_messages.extend(ChatUtils.create_bot_chat_creation_messages(user1, user2, options['bot-message']))

        brian_bot = UserUtils.get_brian_bot()
        for message in bot_messages:
            try:
                MessageService(message.chat, brian_bot, message).on_new_message()
            except:
                pass
