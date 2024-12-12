from django import template

register = template.Library()


@register.filter
def get_range(value):
    """
    Returns a range from 1 to `value` (inclusive).
    """
    return range(1, value + 1)


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, [])
    except AttributeError:
        return []


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
