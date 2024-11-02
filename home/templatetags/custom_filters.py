from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg
# myapp/templatetags/custom_filters.py


@register.filter
def split_words(value):
    """Return the first two words and the remaining string."""
    words = value.split()
    first_two = ' '.join(words[:2])  # Join first two words
    remaining = ' '.join(words[2:])  # Join remaining words
    return first_two, remaining

@register.filter
def display_page(page, page_obj):
    return page <= 2 or page >= page_obj.paginator.num_pages - 1 or (page_obj.number - 1 <= page <= page_obj.number + 1)

