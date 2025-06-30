from django.contrib.contenttypes.models import ContentType
from core.models import Event

def log_event(actor, action, instance, notes=None):
    """
    Generic utility to log an event on any model instance.

    :param actor: User instance who performed the action
    :param action: String like "Created", "Updated", "Deleted"
    :param instance: The model instance the event is linked to
    :param notes: Optional details
    """
    Event.objects.create(
        actor=actor,
        action=action,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        notes=notes
    )

