from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from enum import Enum

User = get_user_model()


class Trackable(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        abstract = True  # Use True if you only want to inherit from it

    def __str__(self):
        return self.title
    

class TrackableStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class TrackableUrgency(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class TrackableClassification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class EventActions(str, Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"
    COMPLETED = "Completed"
    ASSIGNED = "Assigned"
    

class Event(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)  # e.g. "Created", "Updated", etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    # Generic relation to any object (task, project, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.content_object}"