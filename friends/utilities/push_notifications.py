import logging
import requests

from ..settings import base
from ..serializers import LuminosUserPartnerSerializer

NEW_MESSAGE_NOTIFICATION = 'NEW_MESSAGE_NOTIFICATION'
FEEDBACK_REQUEST_NOTIFICATION = 'FEEDBACK_REQUEST_NOTIFICATION'


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

    def build_new_message_notification_body(self, message, recipient, feedback_requested):
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
            "android_group": "{0}-{1}".format(NEW_MESSAGE_NOTIFICATION, message.chat.id),
            "android_group_message": {
                "en": "You have $[notif_count] new messages from {0}".format(message.sender.first_name)},
            "thread_id": "{0}-{1}".format(NEW_MESSAGE_NOTIFICATION, message.chat.id),
            "summary_arg": message.sender.first_name,
            "ios_badgeType": "Increase",
            "ios_badgeCount": 1,
            "data": {
                "type": NEW_MESSAGE_NOTIFICATION,
                "chat_type": message.chat.type,
                "round_id": message.chat.round,
                "chat_id": message.chat.id,
                "message_id": message.id,
                "message_sender": LuminosUserPartnerSerializer(message.sender).data,
                "message_recipient": LuminosUserPartnerSerializer(recipient).data,
                "message_text": message.text,
                "message_timestamp": message.timestamp.isoformat(),
                "feedback_requested": feedback_requested
            }
        }

    def dispatch_new_message_notification(self, message, recipient_chatuser):
        if base.ONESIGNAL_DISABLE == "1":
            return

        notification_body = self.build_new_message_notification_body(message, recipient_chatuser.user,
                                                                     recipient_chatuser.feedback_requested)
        return self.dispatch_notification(notification_body)

    def build_feedback_request_notification_body(self, luminos_bot_message, chat, recipient):
        body = self.build_new_message_notification_body(luminos_bot_message, recipient, False)

        body["data"]["type"] = FEEDBACK_REQUEST_NOTIFICATION
        body["data"]["feedback_requested_for_chat"] = chat.id
        return body

    def dispatch_feedback_request_notification(self, luminos_bot_message, chat, recipient):
        if base.ONESIGNAL_DISABLE == "1":
            return

        notification_body = self.build_feedback_request_notification_body(luminos_bot_message, chat, recipient)
        return self.dispatch_notification(notification_body)
