
from django.conf.urls import include
try:
    from django.conf.urls.defaults import patterns#, url
except ImportError:
    from django.conf.urls import patterns#, url
from django.contrib import admin

admin.autodiscover()

#import helpdesk

urlpatterns = patterns('helpdesk.tests.views',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('helpdesk.urls')),
)
