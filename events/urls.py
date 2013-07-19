from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
      url(r'fullcalendar/$', 'fullcalendar_data', name='fullcalendar'),
)

