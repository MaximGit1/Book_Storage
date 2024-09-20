from django import template
from django.utils.safestring import mark_safe
from markdown import markdown


register = template.Library()

@register.filter(name='markdown')
def markdown_format(text: str) -> str:
    return mark_safe(markdown(text))