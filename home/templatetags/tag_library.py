from django import template

register = template.Library()

@register.filter()
def to_int_progress(value):
    new = 100/int(value)
    return int(new)