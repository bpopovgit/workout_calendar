from django import template

register = template.Library()

@register.filter
def get_range(value):
    """
    Returns a range from 1 to `value` (inclusive).
    """
    return range(1, value + 1)
