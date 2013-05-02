from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
      url(r'coming-soon/$', 'coming_soon', name=''),
)

