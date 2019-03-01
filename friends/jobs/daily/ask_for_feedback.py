import datetime
import logging

from django_extensions.management.jobs import BaseJob

from friends import models
from friends.utilities.push_notifications import NotificationService

class Job(BaseJob):
    help = "Ask users for feedback."
    def __init__(self, ignore_calendar=False):
        super().__init__()
        self.ignore_calendar = ignore_calendar

    def should_we_execute(self):
        if self.ignore_calendar:
            return True

        return datetime.datetime.now().weekday() == 3

    def execute(self):
        if not self.should_we_execute():
            self.stdout.write("I only run on Thursdays")
            return

        chats = models.Chat.objects.filter(round=1, chatusers__feedback_requested=False)

        for chat in chats:
            if self.all_users_participated(chat):
                self.ask_for_feedback(chat)

    def all_users_participated(self, chat):
        for chatuser in chat.chatusers_set.all():
            if not models.Message.objects.filter(chat_id=chat.id, sender=chatuser.user).exists():
                return False
        return True

    def ask_for_feedback(self, chat):
        for chatuser in chat.chatusers_set.all():
            logging.log(logging.INFO, f"Asking user {chatuser.user_id} for feedback in chat {chatuser.chat_id}")
            chatuser.feedback_requested = True
            chatuser.save()
            self.notify_participant(chat, chatuser.user)

    def notify_participant(self, chat, user):
        NotificationService().dispatch_feedback_request_notification(chat, user)
