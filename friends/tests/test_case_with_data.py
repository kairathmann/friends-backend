from django.test import TestCase
from rest_framework.authtoken.models import Token
from .. import models


class TestCaseWithData(TestCase):
    def setUp(self):
        # Remove colors that are inserted by default (8 basic ones)
        models.Color.objects.all().delete()
        models.Color.objects.create(id=1, hex_value='AABBCC')
        models.Color.objects.create(id=2, hex_value='ABABAB')
        # Remove questions that are inserted by default
        models.SurveyQuestion.objects.all().delete()

    def tearDown(self):
        models.Chat.objects.all().delete()
        models.Round.objects.all().delete()
        models.LunaUser.objects.all().delete()
        models.SurveyQuestion.objects.all().delete()
        models.SurveyAnswer.objects.all().delete()
        models.SurveyResponse.objects.all().delete()
        models.Color.objects.all().delete()

    def addRounds(self):
        self.round1 = models.Round.objects.create(
            description='description1',
        )
        self.round2 = models.Round.objects.create(
            description='description2',
        )

    def addSurvey(self, add_responses=True):
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
        if add_responses:
            self.response2 = models.SurveyResponse.objects.create(
                user=self.user,
                answer=self.answer2a,
            )

            # Response 2b is current response now as is created a few ms after response2
            self.response2b = models.SurveyResponse.objects.create(
                user=self.user,
                answer=self.answer2b,
            )

    def addMultiResponseQuestion(self):
        self.multi_response_question1 = models.SurveyQuestion.objects.create(
            text='multi response question text',
            max_answers=2,
        )

    def addAuthenticatedUser(self):
        self.user = models.LunaUser.objects.create_user(
            username='test',
            city='test-city',
            first_name='Test Name',
            email='test@example.com',
            color=models.Color.objects.get(id=1),
            emoji='😪',
            password='test')
        self.token = Token.objects.get(user=self.user).key
        self.header = {'HTTP_AUTHORIZATION': "Bearer {}".format(self.token)}

    def addMoreUsers(self):
        self.user2 = models.LunaUser.objects.create_user(
            username='test2',
            city='test-city',
            first_name='Second',
            email='test2@example.com',
            color=models.Color.objects.get(id=2),
            emoji='🤠',
            password='test')

        self.user3 = models.LunaUser.objects.create_user(
            username='test3',
            city='test-city',
            first_name='Third',
            email='test3@example.com',
            color=models.Color.objects.get(id=2),
            emoji='🤠',
            password='test')

    def addLegacyUsers(self):
        self.legacy_user = models.LunaUser.objects.create_user(
            username='legacy@example.com')

        self.migrated_legacy_user = models.LunaUser.objects.create_user(
            username='+490123456789',
            email='migrated.legacy@example.com', )

    def addChat(self, users, round=None):
        self.chat1 = models.Chat.objects.create(
            round=round,
            initial_type=models.CHAT_TYPE_TEXT,
            type=models.CHAT_TYPE_TEXT
        )

        # We need the DB to assign a chat ID before we can use it in Many-to-Many relations.
        self.chat1.save()
        for u in users:
            models.ChatUsers.objects.create(chat=self.chat1, user=u)

    def addMessage(self):
        self.message = models.Message.objects.create(
            chat=self.chat1,
            sender=self.user,
            text="Hello World!",
        )

    def addSecondMessage(self):
        self.message2 = models.Message.objects.create(
            chat=self.chat1,
            sender=self.user,
            text="Hello World Again!",
        )
