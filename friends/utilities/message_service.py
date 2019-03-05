from .push_notifications import NotificationService


class MessageService:

    def __init__(self, chat, user, message):
        self.chat = chat
        self.user = user
        self.message = message

    def on_new_message(self):
        self.update_last_read()
        self.notify_all_users()

    def on_message_read(self):
        self.update_last_read()

    def update_last_read(self):
        chat_user = self.chat.chatusers_set.get(user=self.user)
        chat_user.last_read = self.message
        chat_user.save()

    def notify_all_users(self):
        for chatuser in self.chat.chatusers_set.all():
            if chatuser.user.id != self.user.id:
                NotificationService().dispatch_new_message_notification(self.message, chatuser.user)
