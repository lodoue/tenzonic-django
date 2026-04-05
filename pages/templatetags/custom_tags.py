# In your app's templatetags/custom_tags.py
from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def get_obj_attr(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.inclusion_tag('tags/rating_star.html')
def show_rating(rating):
    filled = int(rating)
    half = 1 if rating-filled > 0 else 0
    empty = int(5-(filled+half))

    return {
        'rated': rating,
        'filled': list(range(0, filled, 1)), 
        'half': list(range(0, half, 1)),
        'empty': list(range(0, empty, 1))
    }