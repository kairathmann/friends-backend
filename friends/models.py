from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

CITY_MAX_LENGTH = 35

# From django.contrib.auth.models.AbstractUser
FIRST_NAME_MAX_LENGTH = 30

SURVEY_ANSWER_TEXT_MAX_LENGTH = 255

SURVEY_QUESTION_TEXT_MAX_LENGTH = 255


class LunaUser(AbstractUser):
    """
    The username is the user's phone number in E164 format.
    """

    city = models.CharField(max_length=CITY_MAX_LENGTH, db_index=True)


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    answer = models.ForeignKey(SurveyAnswer, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)


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
