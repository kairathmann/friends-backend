import logging
import requests

from ..settings import base
from ..serializers import LunaUserPartnerSerializer


class NotificationService:

    def build_notification_body(self, message, recipient):
        return {
            "app_id": base.ONESIGNAL_APPID,
            "headings": {
                "en": message.sender.first_name,
            },
            "include_external_user_ids": [str(recipient.id)],
            "contents": {
                "en": message.text,
            },
            "isEmail": False,
            "android_group": message.chat.id,
            "android_group_message": {"en": "You have $[notif_count] new messages from {0}".format(message.sender.first_name)},
            "thread_id": message.chat.id,
            "summary_arg": message.sender.first_name,
            "data": {
                "chat_type": message.chat.type,
                "chat_id": message.chat.id,
                "message_id": message.id,
                "message_sender": LunaUserPartnerSerializer(message.sender).data,
                "message_recipient": LunaUserPartnerSerializer(recipient).data,
                "message_text": message.text,
                "message_timestamp": str(message.timestamp),
            }
        }

    def dispatch_notification(self, message, recipient):
        """
        Calls OneSignal API to send push notification to recipient
        """

        if base.ONESIGNAL_DISABLE == "1":
            return

        message_body = self.build_notification_body(message, recipient)

        try:
            response = requests.post(
                base.ONESIGNAL_API_ENDPOINT,
                headers={
                    "Authorization": base.ONESIGNAL_AUTHORIZATION_HEADER,
                    "Content-Type": "application/json; charset=utf-8"
                },
                json=message_body,
            )
        except requests.exceptions.RequestException as exc:
            logging.log(logging.WARNING, f'failed to send a notification: {exc}')

