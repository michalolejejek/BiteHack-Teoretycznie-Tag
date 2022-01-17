from typing import List

from shargain.notifications.models import NotificationChannelChoices
from shargain.notifications.senders import TelegramNotificationSender
from shargain.offers.models import Offer, ScrappingTarget


class NewOfferNotificationService:
    def __init__(self, offers: List[Offer], scrapping_target: ScrappingTarget):
        assert (
            scrapping_target.notification_config_id
        ), "Scrapping target has no notification_config"
        self.offers = offers
        self._scrapping_target = scrapping_target

    def run(self):
        message = self.get_message_header()
        for offer in self.offers:
            offer_message = self.get_message_for_offer(offer)
            if len(message + offer_message) > self.get_maximum_message_length(
                self._scrapping_target.notification_config.channel  # type: ignore
            ):
                self._send(message)
                message = self.get_message_header() + offer_message
            else:
                message += offer_message
        self._send(message)

    def _send(self, message):
        notification_sender = self._get_notification_sender_class()(
            self._scrapping_target.notification_config
        )
        notification_sender.send(message)

    def _get_notification_sender_class(self):
        return self.get_notification_sender_class(
            self._scrapping_target.notification_config.channel  # type: ignore
        )

    @staticmethod
    def get_maximum_message_length(notification_channel):
        return {NotificationChannelChoices.TELEGRAM: 4096}[notification_channel]

    @staticmethod
    def get_notification_sender_class(notification_channel):
        return {NotificationChannelChoices.TELEGRAM: TelegramNotificationSender}[
            notification_channel
        ]

    def get_message_for_offer(self, offer):
        return (
            f"{offer.title} ({offer.published_at.time()}) "
            f"za {offer.price}zł\n{offer.url}\n\n"
        )

    def get_message_header(self):
        return f"{self._scrapping_target.name.upper()}\n\n"
