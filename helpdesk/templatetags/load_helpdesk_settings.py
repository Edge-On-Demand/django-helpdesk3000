"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

templatetags/load_helpdesk_settings.py - returns the settings as defined in 
                                    django-helpdesk/helpdesk/settings.py
"""
from __future__ import print_function

import sys

from django.template import Library
from django.utils.safestring import mark_safe

from helpdesk import settings as helpdesk_settings_config


def load_helpdesk_settings(request):
    try:
        return helpdesk_settings_config
    except Exception as e:
        print("'load_helpdesk_settings' template tag "
              "(django-helpdesk) crashed with following error:", file=sys.stderr)
        print(e, file=sys.stderr)
        return ''


register = Library()
register.filter('load_helpdesk_settings', load_helpdesk_settings)


@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))
