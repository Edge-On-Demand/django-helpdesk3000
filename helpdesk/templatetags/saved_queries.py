"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

templatetags/saved_queries.py - This template tag returns previously saved 
                                queries. Therefore you don't need to modify
                                any views.
"""
import sys
import traceback

from django.template import Library
from django.db.models import Q

from helpdesk.models import SavedSearch

import six

def saved_queries(request):
    try:
        if not request.user.is_authenticated():
            return ''
        user_saved_queries = SavedSearch.objects.filter(Q(user=request.user) | Q(shared__exact=True))
        return user_saved_queries
    except Exception as e:
        six.print_("Error in 'saved_queries' template tag (django-helpdesk):", file=sys.stderr)
        traceback.print_exc()
        return ''

register = Library()
register.filter('saved_queries', saved_queries)
