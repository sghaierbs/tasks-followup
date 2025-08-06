# notifications/utils.py

from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def create_and_send_notification(user,created_by, notif_type, title, message, related_object=None):
    content_type = ContentType.objects.get_for_model(related_object) if related_object else None
    object_id = related_object.id if related_object else None

    notification = Notification.objects.create(
        user=user,
        created_by=created_by,
        notification_type=notif_type,
        title=title,
        message=message,
        content_type=content_type,
        object_id=object_id,
    )

    # Send over WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send.notification",
            "data": {
                "id": notification.id,
                "title": title,
                "created_by":created_by.get_full_name(),
                "message": message,
                "type": notif_type,
                "created_at": notification.created_at.isoformat(),
                "related_model": content_type.model if content_type else None,
                "related_id": object_id,
            }
        }
    )
