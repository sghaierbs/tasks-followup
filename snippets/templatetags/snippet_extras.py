from django import template

register = template.Library()

@register.filter
def split(value, sep=','):
    if value:
        return [item.strip() for item in value.split(sep)]
    return []