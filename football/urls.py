from django.conf.urls import patterns, include, url

urlpatterns = patterns('football.views',
	url(r'^$', 'football', name='football'),
	url(r'^my/predictions/$', 'my_predictions', name='my_predictions'),
	url(r'^matches/$', 'matches', name='matches'),
	url(r'^(?P<id>\d+)/league/$', 'league', name='league'),
	url(r'^(?P<id>\d+)/predictions/$', 'predictions', name='predictions'),
)