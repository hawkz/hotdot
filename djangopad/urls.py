import os
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings



urlpatterns = patterns('',
    url(r'^$', 'pads.views.index', name="pads_list" ),
    (r'^pads/', include('pads.urls') ),
    (r'^accounts/', include('registration.urls') ),
    (r'^admin/(.*)', admin.site.root ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)', 'django.views.static.serve', {'document_root': os.path.join(".", 'static')}),
)

