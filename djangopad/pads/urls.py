from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^new/$', 'pads.views.new', name='pads_new'),
    url(r'^(?P<owner>[-\w]+)/(?P<slug>[-\w]+)/$', 'pads.views.detail',
        name='pads_detail'),
)
