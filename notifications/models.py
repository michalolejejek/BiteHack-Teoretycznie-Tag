from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationChannelChoices(models.TextChoices):
    DISCORD = "discord", "Discord"
    TELEGRAM = "telegram", "Telegram"


class NotificationConfig(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    channel = models.CharField(
        verbose_name=_("Channel"),
        max_length=200,
        choices=NotificationChannelChoices.choices,
    )
    webhook_url = models.URLField(verbose_name=_("Webhook url"), blank=True)
    token = models.CharField(verbose_name=_("Token"), max_length=100, blank=True)
    chatid = models.CharField(verbose_name=_("Chat ID"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("Notification channel")
        verbose_name_plural = _("Notification channels")

    def __str__(self):
        return self.name
