from django.db import models
from core.models import TrackableStatus, TrackableUrgency
from sprints.models import Sprint
from django.contrib.auth.models import User
from django.db.models import Min, Max


def get_default_status():
    status = TrackableStatus.objects.filter(name='New').first()
    status_id = status.id if status else None
    return status_id

def get_default_urgency():
    urgency = TrackableUrgency.objects.filter(name='Medium').first()
    urgency_id = urgency.id if urgency else None
    return urgency_id

class UserStory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sprint = models.ForeignKey(Sprint, related_name='user_stories', on_delete=models.CASCADE)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    #status = models.ForeignKey(TrackableStatus, on_delete=models.SET_NULL, null=True, default=get_default_status)
    status = models.CharField(blank=True, max_length=200)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stories')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    urgency = models.ForeignKey(TrackableUrgency, on_delete=models.SET_NULL, null=True, default=get_default_urgency)

    def __str__(self):
        return self.title
  