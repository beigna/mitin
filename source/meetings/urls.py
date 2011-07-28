
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('meetings.views',
    url(r'^guest_confirm/$', 'guest_confirm', name='meetings_guest_confirm'),
)
