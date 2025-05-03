from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Splits a string by the given separator."""
    if not value:
        return []
    return value.split(arg)



@register.filter
def strip(value):
    """Strips whitespace from a string."""
    if isinstance(value, str):
        return value.strip()
    return value



