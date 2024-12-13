from django import template

register = template.Library()


@register.filter
def duration_to_minutes(value):
    if value:
        total_seconds = value.total_seconds()
        minutes = int(total_seconds // 60)
        return f"{minutes} minutes"
    return "N/A"


@register.filter
def format_duration(value):
    """
    Formats a duration as 'X hours Y minutes' or 'X minutes' if less than an hour.
    """
    total_seconds = int(value.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minute{'s' if minutes > 1 else ''}"
        return f"{hours} hour{'s' if hours > 1 else ''}"
    return f"{minutes} minute{'s' if minutes > 1 else ''}"
