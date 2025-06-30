from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import TrackableStatus, TrackableUrgency, TrackableClassification
import logging


"""
This is a signal which will try to poplate the database with the initial data required for the application to run 
1- Status
2- Urgency
3- Classification
"""
logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_default_statuses(sender, **kwargs):
    default_statuses = ['In Progress', 'Resolved', 'Closed', 'New', 'Archived']
    logger.info("Populating database with initial status.")
    for status in default_statuses:
        logger.info(f"Inserting the status: {status} to table core_trackablestatus.")
        TrackableStatus.objects.get_or_create(name=status)


@receiver(post_migrate)
def create_default_urgency(sender, **kwargs):
    default_urgency = ['Low', 'Medium', 'High']
    logger.info("Populating database with initial urgency.")
    for urgency in default_urgency:
        logger.info(f"Inserting the urgency: {urgency} to table core_trackableurgency.")
        TrackableUrgency.objects.get_or_create(name=urgency)



@receiver(post_migrate)
def create_default_urgency(sender, **kwargs):
    default_classification = ['Business', 'Technical', 'External communication', 'Internal communication', 'Followup', 'Reminder']
    logger.info("Populating database with initial classification.")
    for classification in default_classification:
        logger.info(f"Inserting the classification: {classification} to table core_trackableclassification.")
        TrackableClassification.objects.get_or_create(name=classification)
