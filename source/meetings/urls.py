
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('meetings.views',
    url(r'^$', 'list', name='meetings_list'),
    url(r'^create/$', 'create', name='meetings_create'),
    url(r'^confirm/$', 'confirm', name='meetings_confirm'),
    url(r'^respond/$', 'respond', name='meetings_respond'),
)
