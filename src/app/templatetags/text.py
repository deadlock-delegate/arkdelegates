from django import template


register = template.Library()


@register.filter(name="replace")
def replace(value, replace_args):
    old, new = replace_args.split(",")
    return str(value).replace(old, new)
