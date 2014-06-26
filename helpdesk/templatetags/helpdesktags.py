"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

templatetags/in_list.py - Very simple template tag to allow us to use the
                          equivilent of 'if x in y' in templates. eg:

Assuming 'food' = 'pizza' and 'best_foods' = ['pizza', 'pie', 'cake]:

{% if food|in_list:best_foods %}
 You've selected one of our favourite foods!
{% else %}
 Your food isn't one of our favourites.
{% endif %}
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def nbsp(s):
    return mark_safe(s.replace(' ', '&nbsp;'))
