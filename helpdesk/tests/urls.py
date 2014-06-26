
from django.conf.urls import *
from django.contrib import admin

admin.autodiscover()

#import helpdesk

urlpatterns = patterns('helpdesk.tests.views',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('helpdesk.urls')),
)
