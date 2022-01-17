from django.contrib import admin

from shargain.notifications.models import NotificationConfig


@admin.register(NotificationConfig)
class NotificationConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "channel")
