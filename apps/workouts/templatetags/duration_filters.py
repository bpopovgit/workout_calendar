from django import template

register = template.Library()


@register.filter
def duration_to_minutes(value):
    if value:
        total_seconds = value.total_seconds()
        minutes = int(total_seconds // 60)
        return f"{minutes} minutes"
    return "N/A"
