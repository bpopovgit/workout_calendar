from django import template

register = template.Library()


@register.simple_tag
def query_string(request, **kwargs):
    """
    Generates a query string with updated GET parameters.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, None)
    return updated.urlencode()