import logging
import requests

from ..settings import base
from ..serializers import LunaUserPartnerSerializer


class NotificationService:
    def dispatch_notification(self, notification_body):
        """
        Calls OneSignal API to send push notification to recipient
        """
        try:
            response = requests.post(
                base.ONESIGNAL_API_ENDPOINT,
                headers={
                    "Authorization": base.ONESIGNAL_AUTHORIZATION_HEADER,
                    "Content-Type": "application/json; charset=utf-8"
                },
                json=notification_body,
            )
        except requests.exceptions.RequestException as exc:
            logging.log(logging.WARNING, f'failed to send a notification: {exc}')

        return response


    def build_new_message_notification_body(self, message, recipient):
        return {
            "app_id": base.ONESIGNAL_APPID,
            "headings": {
                "en": message.sender.first_name,
            },
            "include_external_user_ids": [str(recipient.notification_id)],
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
                "round_id": message.chat.round,
                "chat_id": message.chat.id,
                "message_id": message.id,
                "message_sender": LunaUserPartnerSerializer(message.sender).data,
                "message_recipient": LunaUserPartnerSerializer(recipient).data,
                "message_text": message.text,
                "message_timestamp": message.timestamp.isoformat()
            }
        }


    def dispatch_new_message_notification(self, message, recipient):
        if base.ONESIGNAL_DISABLE == "1":
            return

        notification_body = self.build_new_message_notification_body(message, recipient)
        return self.dispatch_notification(notification_body)


    def build_feedback_request_notification_body(self, chat, recipient):
        return {
            "app_id": base.ONESIGNAL_APPID,
            "headings": {
                "en": 'I CAN HAZ FEEDBACK' #TODO
            },
            "include_external_user_ids": [str(recipient.notification_id)],
            "contents": {
                "en": 'FOR REALZ, I CAN HAZ FEEDBACK???!?',
            },
            "isEmail": False,
            "thread_id": chat.id,
            "data": {
                "chat_id": chat.id,
            }
        }


    def dispatch_feedback_request_notification(self, chat, recipient):
        if base.ONESIGNAL_DISABLE == "1":
            return

        notification_body = self.build_feedback_request_notification_body(chat, recipient)
        return self.dispatch_notification(notification_body)
