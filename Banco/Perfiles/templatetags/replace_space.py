from django import template

register = template.Library()

@register.filter
def replace_space(value):
    return value.replace("\u00A0", ".")