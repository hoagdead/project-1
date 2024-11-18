from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def days_since(value):
    if not value:
        return ""
    now = timezone.now()
    delta = now - value
    days = delta.days

    # Trả về chuỗi tiếng Việt
    if days == 0:
        return "Hôm nay"
    elif days == 1:
        return "1 ngày trước"
    else:
        return f"{days} ngày trước"