from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token
import uuid
from .utilities.chat_utils import ChatUtils
from .utilities.user_utils import UserUtils

CITY_MAX_LENGTH = 100

# From django.db.models.fields.EmailField
EMAIL_MAX_LENGTH = 254

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

COLOR_MAX_LENGTH = 6
EMOJI_MAX_LENGTH = 4


class Color(models.Model):
    """
    A color is a user selected color that is used as a part of user avatar and used to style parts of application according to user selection.
    """
    hex_value = models.CharField(max_length=COLOR_MAX_LENGTH, unique=True)
    brian_bot = models.BooleanField(default=False)  # For the special Brian Bot color (not available to other users)


class LunaUser(AbstractUser):
    """
    The username is the user's phone number in E164 format.
    """

    color = models.ForeignKey(Color, null=True, on_delete=models.PROTECT)
    emoji = models.CharField(max_length=EMOJI_MAX_LENGTH)
    is_brian_bot = models.BooleanField(default=False)
    notification_id = models.UUIDField(null=False, default=uuid.uuid4, unique=True)


class Location(models.Model):
    """
    Location is user's city of choice used for matching via proximity etc.

        full_name: value displayed for user at dropdown - 'Warszawa, Mazowieckie, Poland'
        name: short-hand value of location - 'Warszawa'
        mapbox_id: Unique identifier of Geolocation object returned from Mapbox API - storing in case of future needs - 'place.12284077938513600'
        latitude: Floating-point value between 0 and 90 degrees - 21.03333 
        longitude: Floating-point value between -180 and 180 degrees - 52.21667
    """

    mapbox_id = models.CharField(max_length=255)
    name = models.CharField(max_length=CITY_MAX_LENGTH)
    full_name = models.CharField(max_length=CITY_MAX_LENGTH)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(LunaUser, on_delete=models.CASCADE)

    def __eq__(self, other):
        return self.mapbox_id == other.mapbox_id


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


class SurveyQuestion(models.Model):
    """
    A SurveyQuestion is a multiple-choice question. One SurveyQuestion object has several SurveyAnswer objects
    referencing it.
    """

    text = models.CharField(max_length=SURVEY_QUESTION_TEXT_MAX_LENGTH, unique=True)

    # The maximum number of answers a user may select for this question.
    max_answers = models.PositiveSmallIntegerField(default=1)

    is_enabled = models.BooleanField(default=True)


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

    text = models.CharField(max_length=FREE_TEXT_QUESTION_MAX_LENGTH, unique=True)


class FreeTextResponse(models.Model):
    """
    A FreeTextResponse is one user's individual free text answer to a FreeTextQuestion.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    question = models.ForeignKey(FreeTextQuestion, related_name='responses', on_delete=models.CASCADE)

    text = models.TextField()

    timestamp = models.DateTimeField(default=timezone.now, db_index=True, editable=False)


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

    # 1 for the current match chat, None for everything else
    round = models.PositiveSmallIntegerField(null=True)

    # The type that was initially set for this chat during a Round, if applicable.
    # Only used for data analysis.
    initial_type = models.PositiveSmallIntegerField(choices=CHAT_TYPES)

    # The current type of this chat. Returned by the API.
    type = models.PositiveSmallIntegerField(choices=CHAT_TYPES)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

    # null for system messages
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    text = models.TextField()

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)


class ChatUsers(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # There may be a clever trigger on on_delete to find the next last-read message.
    last_read = models.ForeignKey(Message, null=True, on_delete=models.SET_NULL)

    # This flag set to True on when we have requested the user to give us feedback about the chat partner, and cleared
    # back to False when the user has given feedback.
    feedback_requested = models.BooleanField(default=False)

    class Meta:
        unique_together = ('chat', 'user')


FEEDBACK_QUESTION_TEXT_MAX_LENGTH = 255
FEEDBACK_TYPE_RATING = 1
FEEDBACK_TYPE_TEXT = 2

FEEDBACK_TYPES = (
    (FEEDBACK_TYPE_RATING, "Rating"),
    (FEEDBACK_TYPE_TEXT, "Text"),
)

MIN_FEEDBACK_RATING = 1
MAX_FEEDBACK_RATING = 5


class FeedbackQuestion(models.Model):
    text = models.CharField(max_length=FEEDBACK_QUESTION_TEXT_MAX_LENGTH, unique=True)

    order_index = models.PositiveSmallIntegerField(db_index=True, unique=True)

    type = models.PositiveSmallIntegerField(choices=FEEDBACK_TYPES)

    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ['order_index', ]

    def __str__(self):
        return self.text


class FeedbackResponse(models.Model):
    question = models.ForeignKey(FeedbackQuestion, related_name='feedback_responses', on_delete=models.CASCADE)

    chat_user = models.ForeignKey(ChatUsers, null=True, blank=True, on_delete=models.SET_NULL)

    rating_response = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(MIN_FEEDBACK_RATING), MaxValueValidator(MAX_FEEDBACK_RATING)]
    )

    text_response = models.TextField(null=True, blank=True)


TERMS_TYPE_TERMS_OF_SERVICE = 1
TERMS_TYPE_PRIVACY_POLICY = 2
TERMS_TYPES = (
    (TERMS_TYPE_TERMS_OF_SERVICE, "Terms of Service"),
    (TERMS_TYPE_PRIVACY_POLICY, "Privacy Policy"),
)


# For now we won't load ToS and PP via a REST endpoint but hardcode it in the mobile app.
class Terms(models.Model):
    """
    Represents a Terms and Conditions or Privacy Policy text that a user can agree to.
    """

    text = models.TextField()

    type = models.PositiveSmallIntegerField(choices=TERMS_TYPES)

    # Current terms are auto-assigned to new users.
    # One does not simply change the current terms.
    # New terms will need a new API and mobile app release.
    is_current = models.BooleanField(default=False)


class UserTermsAcceptance(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)

    accepted_timestamp = models.DateTimeField(default=timezone.now, db_index=True, editable=False)


class PhoneVerificationExemption(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    country_code = models.CharField(max_length=5)

    phone_number = models.CharField(max_length=18)

    token = models.CharField(max_length=4)


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
@transaction.atomic
def handle_new_user(sender, instance=None, created=False, **kwargs):
    """
    This function contains actions to perform upon user creation.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        # Auth Token
        Token.objects.get_or_create(user=instance)

        # Create a Brian Bot Chat with any non-staff user.
        # Staff users are the Brian Bot itself and any superusers created on the commandline.
        if not instance.is_staff:
            brian_bot = UserUtils.get_brian_bot()
            ChatUtils.create_chat([brian_bot, instance], 'Welcome to Luminos! If you have any questions, suggestions, or even if you just want to chat, you can message us anytime!')
