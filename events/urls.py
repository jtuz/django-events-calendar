from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
      url(r'fullcalendar/$', 'fullcalendar_data', name='fullcalendar'),
      url(r'current/(?P<slug>[a-zA-Z0-9\-]+)$', 'event', name='event'),
)

