# tasks/templatetags/task_extras.py
from django import template

register = template.Library()

@register.filter
def status_class(status):
    if hasattr(status, 'name'):
        # It's a TrackableStatus object
        status_name = status.name
    else:
        # It's a string
        status_name = status
    return {
        'New': 'bg-primary',
        'Closed': 'bg-success',
        'In Progress': 'bg-warning text-dark',
        'Resolved': 'bg-info text-dark',
    }.get(status_name, '')

@register.filter
def status_filter_class(status):
    if hasattr(status, 'name'):
        # It's a TrackableStatus object
        status_name = status.name
    else:
        # It's a string
        status_name = status
    return  {
        'All': 'btn-outline-primary',
        'New': 'btn-outline-primary',
        'Closed': 'btn-outline-success',
        'In Progress': 'btn-outline-warning',
        'Archived': 'btn-outline-secondary',
        'Resolved': 'btn-outline-info',
    }.get(status_name, '')

@register.filter
def urgency_class(urgency):
    return {
        'High': 'bg-danger text-light',
        'Medium': 'bg-primary',
        'Low': 'bg-success',
    }.get(urgency.name, '')