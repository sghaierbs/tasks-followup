from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Min, Max
from .models import Assignment, UserStory
from django.db import transaction


def update_user_story_dates(user_story):
    actual_dates = user_story.assignments.aggregate(
        earliest=Min('start_date'),
        latest=Max('end_date')
    )
    user_story.start_date = actual_dates['earliest']
    user_story.end_date = actual_dates['latest']
    planned_dates = user_story.assignments.aggregate(
        earliest=Min('planned_start_date'),
        latest=Max('planned_end_date')
    )
    user_story.planned_start_date = planned_dates['earliest']
    user_story.planned_end_date = planned_dates['latest']
    
    user_story.save(update_fields=['start_date', 'end_date', 'planned_start_date', 'planned_end_date'])


@receiver(post_save, sender=Assignment)
@receiver(post_delete, sender=Assignment)
def assignment_changed(sender, instance, **kwargs):
    if instance.user_story:
        update_user_story_dates(instance.user_story)


@receiver(post_save, sender=Assignment)
@receiver(post_delete, sender=Assignment)
def update_user_story_status_on_assignment_save(sender, instance, **kwargs):
    from .utils import update_user_story_status  # Avoid circular import
    # Ensure update happens after transaction completes (e.g. inside view logic)
    transaction.on_commit(lambda: update_user_story_status(instance.user_story))