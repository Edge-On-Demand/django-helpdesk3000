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
import re
import urllib

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def nbsp(s):
    return mark_safe(s.replace(' ', '&nbsp;'))

@register.simple_tag
def sortable_column_link(request, name, sort_param, label=None, default=''):
    sort_order = request.GET.get(sort_param, default or '').split(',')
    sort_order = [_.strip() for _ in sort_order if _.strip()]
    arrow = ''
    #print 'GET:',request.GET
    params = request.GET.copy()
#    print 'params:',params
    
    if name in sort_order:
        arrow = '<b>&uarr;<b/>'
        params[sort_param] = '-'+name
    elif '-'+name in sort_order:
        arrow = '<b>&darr;</b>'
        params[sort_param] = name
    else:
        params[sort_param] = name
    
    params = dict(
        (k, ','.join(map(str, v)) if isinstance(v, list) and len(v) > 1 else (v and v[0]))
        for k,v in params.iterlists())
#    print 'params:',params
    kwargs = dict(
        url=request.path + '?' + urllib.urlencode(params),
        name=re.sub('^[^a-zA-Z#]+', '', label or name),
        arrow=arrow
    )
    return '<a href="{url}">{name}{arrow}</a>'.format(**kwargs)
    