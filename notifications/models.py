from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("task", "Task"),
        ("comment", "Comment"),
        ("reminder", "Reminder"),
        ("custom", "Custom"),
    ]


    # this is the user who is targeted by the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_creator")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return f"To {self.user.username}: {self.message[:50]}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
