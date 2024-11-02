from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def less_than(value, arg):
    """Returns True if value is less than arg."""
    try:
        return float(value) < float(arg)
    except (ValueError, TypeError):
        return False

@register.filter
def between(value, args):
    """Check if value is between two numbers (min, max)."""
    try:
        min_value, max_value = map(float, args.split(','))
        return min_value < float(value) < max_value
    except (ValueError, TypeError):
        return False


@register.filter
def stars_range(rating):
    filled = range(rating)  # Filled stars
    empty = range(5 - rating)  # Empty stars up to 5
    return {'filled': filled, 'empty': empty}
