from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

CITY_MAX_LENGTH = 35

# From django.contrib.auth.models.AbstractUser
FIRST_NAME_MAX_LENGTH = 30

FREE_TEXT_QUESTION_MAX_LENGTH = 255

FREE_TEXT_RESPONSE_MAX_LENGTH = 255

LEGACY_TELEGRAM_MAX_LENGTH = 26

LEGACY_TOKEN_MAX_LENGTH = 32

SURVEY_ANSWER_TEXT_MAX_LENGTH = 255

SURVEY_QUESTION_TEXT_MAX_LENGTH = 255

GENDER_ID_MALE = 1
GENDER_ID_FEMALE = 2
GENDER_ID_OTHER = 3
GENDER_IDS = (
    (GENDER_ID_MALE, 'male'),
    (GENDER_ID_FEMALE, 'female'),
    (GENDER_ID_OTHER, 'other'),
)


class LunaUser(AbstractUser):
    """
    The username is the user's phone number in E164 format.
    """

    city = models.CharField(max_length=CITY_MAX_LENGTH, db_index=True)


class LegacyDataSet(models.Model):
    """
    A LegacyDataSet is the data users gave during the December 2018 Telegram experiments. It only contains those fields
    not used in the standard models.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Product team's internal flag for evaluating users in experiments.
    good_user = models.BooleanField()

    name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)

    # The user's first experiment round.
    entry_round = models.PositiveIntegerField()

    telegram = models.CharField(max_length=LEGACY_TELEGRAM_MAX_LENGTH)

    gender = models.PositiveSmallIntegerField(choices=GENDER_IDS)

    age = models.PositiveSmallIntegerField()

    location = models.CharField(max_length=CITY_MAX_LENGTH)

    # Answer to the question "How well do you think we could match you based on these questions?".
    # Not modeled as a FreeTextQuestion because it is service feedback and dependent on the December 2018 context.
    expect_match_well = models.BooleanField()

    # Answer to the question "What, if anything, do you think is missing from our questions?".
    # Not modeled as a FreeTextQuestion because it is service feedback and dependent on the December 2018 context.
    missing_from_questions = models.TextField(blank=True)

    submitted_at = models.DateTimeField()

    token = models.CharField(max_length=LEGACY_TOKEN_MAX_LENGTH)


@receiver(models.signals.post_save, sender=LunaUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


class SurveyQuestion(models.Model):
    """
    A SurveyQuestion is a multiple-choice question. One SurveyQuestion object has several SurveyAnswer objects
    referencing it.
    """

    text = models.CharField(max_length=SURVEY_QUESTION_TEXT_MAX_LENGTH)

    # The maximum number of answers a user may select for this question.
    max_answers = models.PositiveSmallIntegerField(default=1)


class SurveyAnswer(models.Model):
    """
    A SurveyAnswer is one of several possible answers to a multiple-choice SurveyQuestion.
    """

    question = models.ForeignKey(SurveyQuestion, related_name='answers', on_delete=models.CASCADE)

    order_index = models.PositiveSmallIntegerField(db_index=True)

    text = models.CharField(max_length=SURVEY_ANSWER_TEXT_MAX_LENGTH)

    class Meta:
        ordering = ['order_index', ]
        unique_together = (('question', 'order_index'), ('question', 'text'))


class SurveyResponse(models.Model):
    """
    A SurveyResponse is one user's individual choice of SurveyAnswer to a multiple-choice SurveyQuestion.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    answer = models.ForeignKey(SurveyAnswer, related_name='responses', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True, editable=False)


class FreeTextQuestion(models.Model):
    """
    A FreeTextQuestion is a question allowing a user to type a free text answer.
    """

    text = models.CharField(max_length=FREE_TEXT_QUESTION_MAX_LENGTH)


class FreeTextResponse(models.Model):
    """
    A FreeTextResponse is one user's individual free text answer to a FreeTextQuestion.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    text = models.TextField()

    timestamp = models.DateTimeField(default=timezone.now, db_index=True, editable=False)


class Round(models.Model):
    """
    A Round is one iteration of an experiment pairing users with one another.
    """

    start_timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    end_timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    description = models.TextField(blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rounds', blank=True)

    class Meta:
        ordering = ['start_timestamp', ]

CHAT_TYPE_FREE = 1
CHAT_TYPE_TEXT = 2
CHAT_TYPE_LONGTEXT = 3
CHAT_TYPE_VIDEO = 4

CHAT_TYPES = (
	(CHAT_TYPE_FREE, "Free"),
	(CHAT_TYPE_TEXT, "Text"),
	(CHAT_TYPE_LONGTEXT, "Longtext"),
	(CHAT_TYPE_VIDEO, "Video"),
)

class Chat(models.Model):
    """
    A chat!
    """

    round = models.ForeignKey(Round, null=True, on_delete=models.DO_NOTHING)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')

    # The type that was initially set for this chat during a Round, if applicable.
    # Only used for data analysis.
    initial_type = models.PositiveSmallIntegerField(choices=CHAT_TYPES)

    # The current type of this chat. Returned by the API.
    type = models.PositiveSmallIntegerField(choices=CHAT_TYPES)
