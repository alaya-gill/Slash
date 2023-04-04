from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name='cut')
@stringfilter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '-')

@register.filter(name='unique_id')
@stringfilter
def unique_id(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '#')

@register.filter(name='id_a')
@stringfilter
def id_a(value, arg):
    """Removes all values of arg from the given string"""
    value = 'a#' + value + 'a#'
    return value.replace(arg, 'a#')

@register.filter(name='id_p')
@stringfilter
def id_p(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, 'p#')