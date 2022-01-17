import abc

import telebot

from shargain.notifications.models import NotificationConfig


class BaseNotificationSender(abc.ABC):
    def __init__(self, notification_config: NotificationConfig):
        self._notification_config = notification_config

    def send(self, message: str):
        pass


class TelegramNotificationSender(BaseNotificationSender):
    def send(self, message: str):
        bot = telebot.TeleBot(self._notification_config.token, parse_mode=None)
        bot.send_message(self._notification_config.chatid, message)
