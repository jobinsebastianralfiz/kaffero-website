"""
Custom template tags for the dashboard.
"""
import html
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def decode_icon(value):
    """Decode HTML entities in icon field to render as emoji."""
    if not value:
        return '✨'
    # Decode HTML entities (like &#128203; -> actual emoji)
    decoded = html.unescape(str(value))
    return mark_safe(decoded)
