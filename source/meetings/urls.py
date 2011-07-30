
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('meetings.views',
    url(r'^create/$', 'create', name='meetings_create'),
    url(r'^confirm/$', 'confirm', name='meetings_confirm'),
)
