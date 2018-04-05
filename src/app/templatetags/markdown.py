from django import template
from markdown import markdown as markdown_fn

register = template.Library()


@register.filter(name='markdown')
def markdown(value):
    return markdown_fn(value, extensions=['markdown.extensions.attr_list'])
