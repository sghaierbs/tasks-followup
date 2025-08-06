from .utils.events import log_event
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification
from django.urls import reverse


class EventLoggingMixin:
    def log_event(self, actor, action, instance, notes=None):
        log_event(actor, action, instance, notes)
