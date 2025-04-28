from django import template
import re

register = template.Library()

@register.filter
def replace_semicolons(value):
    return re.sub(r';', ';<br>', value) 



@register.filter
def new_line_filter(value):
    return re.sub(r"\n", '<br>', value)


@register.filter(name='replace')
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)