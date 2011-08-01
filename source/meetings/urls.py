
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('meetings.views',
    url(r'^create/$', 'create', name='meetings_create'),
    url(r'^(?P<slug>[\w\-]+)/update/$', 'update', name='meetings_update'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', 'delete', name='meetings_delete'),

    url(r'^confirm/$', 'confirm', name='meetings_confirm'),
    url(r'^respond/$', 'respond', name='meetings_respond'),

    url(r'^$', 'list', name='meetings_list'),
    url(r'^(?P<slug>[\w\-]+)/$', 'view', name='meetings_view'),
)
