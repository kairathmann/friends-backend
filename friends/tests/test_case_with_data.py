from django.test import TestCase
from rest_framework.authtoken.models import Token
from .. import models


class TestCaseWithData(TestCase):
    def setUp(self):
        # Remove users (i.e. Brian Bot) that are inserted by default
        models.LunaUser.objects.all().delete()

        # Remove colors that are inserted by default
        models.Color.objects.all().delete()
        models.Color.objects.create(id=1, hex_value='AABBCC')
        models.Color.objects.create(id=2, hex_value='ABABAB')
        models.Color.objects.create(id=3, hex_value='623694', brian_bot=True)

        # Remove questions that are inserted by default
        models.SurveyQuestion.objects.all().delete()

    def tearDown(self):
        models.Chat.objects.all().delete()
        models.LunaUser.objects.all().delete()
        models.SurveyQuestion.objects.all().delete()
        models.SurveyAnswer.objects.all().delete()
        models.SurveyResponse.objects.all().delete()
        models.Color.objects.all().delete()

    def addBrianBot(self):
        brian_bot_color = models.Color.objects.get(brian_bot=True)

        self.brianBot = models.LunaUser.objects.create_user(
            username='Brian-Bot',
            city='Luminos',
            emoji='⭐',
            color=brian_bot_color,
            is_staff=True,
        )

    def removeBrianBot(self):
        models.LunaUser.objects.get(is_staff=True).delete()

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

    def addOneUser(self):
        self.user4 = models.LunaUser.objects.create_user(
            username='test4',
            city='test-city',
            first_name='Fourth',
            email='test4@example.com',
            color=models.Color.objects.get(id=2),
            emoji='🤠',
            password='test')
        self.token4 = Token.objects.get(user=self.user4).key
        self.header4 = {'HTTP_AUTHORIZATION': "Bearer {}".format(self.token4)}

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

    def removeChats(self):
        models.Chat.objects.all().delete()

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
