import datetime
import logging

from django_extensions.management.jobs import BaseJob

from friends import models
from friends.utilities.push_notifications import NotificationService
from friends.utilities.user_utils import UserUtils

class Job(BaseJob):
    help = "Ask users for feedback."
    def __init__(self, ignore_calendar=False):
        super().__init__()
        self.ignore_calendar = ignore_calendar

        self.brian_bot = UserUtils.get_brian_bot()

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
        chatusers = chat.chatusers_set.all()[::1]
        chatuser_a = chatusers[0]
        chatuser_b = chatusers[1]
        logging.log(logging.INFO, f"Asking user {chatuser_a.user_id} and {chatuser_b.user_id} for feedback in chat {chat.id}")

        chatuser_a.feedback_requested = True
        chatuser_a.save()
        self.notify_participant(chat, chatuser_a.user, chatuser_b.user)

        chatuser_b.feedback_requested = True
        chatuser_b.save()
        self.notify_participant(chat, chatuser_b.user, chatuser_a.user)

    def notify_participant(self, chat, user, match_partner):
        luminos_bot_message = models.Message.objects.create(
            chat_id=chat.id,
            text=f'How did it go with {match_partner.first_name}? You can now submit feedback on your experience with {match_partner.first_name} to help us improve in the future.',
            sender=self.brian_bot,
        )

        NotificationService().dispatch_feedback_request_notification(luminos_bot_message, chat, user)
