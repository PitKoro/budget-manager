from django import template

register = template.Library()

@register.filter(name='division')
def division(value, args):
    return value/args

@register.filter(name='index_search')
def index_search(arr, index):
    return arr[index]