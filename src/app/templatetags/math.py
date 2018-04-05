from django import template

register = template.Library()

@register.filter(name='divide_by')
def divide_by(value, arg):
    return int(value) / int(arg)
