from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.timezone import now
from core.models import Trackable, TrackableStatus, TrackableUrgency, TrackableClassification, Event
from django.contrib.auth.models import User
from stories.models import UserStory



def get_default_status():
    status = TrackableStatus.objects.filter(name='New').first()
    status_id = status.id if status else None
    return status_id

def get_default_urgency():
    urgency = TrackableUrgency.objects.filter(name='Medium').first()
    urgency_id = urgency.id if urgency else None
    return urgency_id

def get_default_classification():
    classification = TrackableClassification.objects.filter(name='Technical').first()
    classification_id = classification.id if classification else None
    return classification_id

class Task(Trackable):

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(TrackableStatus, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_status)
    urgency = models.ForeignKey(TrackableUrgency, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_urgency)
    classification = models.ForeignKey(TrackableClassification, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_classification)
    assignees = models.ManyToManyField(User, related_name="assigned_tasks", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public', null=True, blank=True)
    user_story = models.ForeignKey(UserStory, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    events = GenericRelation(Event)


    def save(self, *args, **kwargs):

        # Automatically set completed_at when marking as completed
        if self.is_completed and self.completed_at is None:
            self.completed_at = now()
        # If unchecking the task, reset the completed_at
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title + " | "+ self.created_at.strftime('%d/%m/%Y')