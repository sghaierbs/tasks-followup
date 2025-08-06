# tasks/templatetags/task_extras.py
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='truncate')
def truncate(value, max_length):
    if not isinstance(value, str):
        return value
    if len(value) <= max_length:
        return value
    return value[:max_length].rstrip() + '...'