from django.core.management.base import BaseCommand, CommandError
from friends import models
from friends.utilities.message_service import MessageService

TEXT_COLORS = {
    'standard': '\x1b[0m',
    'success': '\x1b[1;32m',
    'warning': '\x1b[1;33m',
    'error': '\x1b[1;31m',
}

class Command(BaseCommand):
    """
    The 'makeglobalannouncement' custom command bulk sends a
    one-to-one message from Brian to every active user.
    :param args: message_text (str).
    :flag args: --test (bool).
    :param options: None.
    :return: Nothing.
    """
    help = 'Sends global message to all Luna users via Brian Bot'

    def add_arguments(self, parser):
        parser.add_argument('message_text',
                            help='The message text to be sent from Brian Bot. '
                                 'Can contain placeholder {user} for the (recipient) user\'s first_name.'
        )
        parser.add_argument('-t', '--test',
                            action='store_true',
                            help='Flag for unit testing. '
                                 'Prevents stdout from being displayed during test case.'
        )

    def handle(self, *args, **options):
        self.message_text = options.get('message_text')
        self.is_test_case = options.get('test')

        # Validate message_text
        if not self.message_text or self.message_text == '':
            self.print_log('Invalid message text. Global announcement not sent.', 'error')
            return

        # Request confirmation from user before sending message (unless test case)
        if self.is_test_case or self.request_confirmation().upper() == 'Y':
            self.send_message()

    def send_message(self):
        self.brian_bot = models.LuminosUser.objects.get(is_brian_bot=True)
        chat_users = models.ChatUsers.objects.filter(user=self.brian_bot)

        message_success_counter = 0
        for chat_user in chat_users:
            recipient_first_name = self.get_recipient_first_name(chat_user)
            try:
                message = models.Message.objects.create(
                    chat=chat_user.chat,
                    sender=self.brian_bot,
                    text=self.message_text.format(user=recipient_first_name),
                )
            except IntegrityError as e:
                self.print_log(f'{e}. Error sending message to chat with id {chat_user.chat.id}', 'error')
            else:
                MessageService(chat_user.chat, self.brian_bot, message).on_new_message()
                message_success_counter += 1

        self.print_log(f'Message successfully sent to {message_success_counter}/{chat_users.count()} chats', 'success')

    def request_confirmation(self):
        self.print_log('You\'re about to send the following message to ALL Luna Users:', 'warning')
        self.print_log(f"'{self.message_text.format(user='<user.first_name>')}'", 'standard')
        self.print_log("Are you sure you want to do this (y/N)? ", 'warning')
        return input()

    def get_recipient_first_name(self, chat_user):
        recipient_chat_user = models.ChatUsers.objects.filter(chat=chat_user.chat).exclude(user=self.brian_bot).first()
        return recipient_chat_user.user.first_name

    def print_log(self, message_text, message_type):
        if not self.is_test_case:
            self.stdout.write(TEXT_COLORS[message_type] + message_text + TEXT_COLORS['standard'])

