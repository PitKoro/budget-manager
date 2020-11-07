from django import template

register = template.Library()

@register.filter(name='division')
def division(value, args):
    return value/args

@register.filter(name='get_value')
def get_value(dict, key):
    return dict[key]