from django.conf.urls import patterns, include, url

urlpatterns = patterns('football.views',
	url(r'^$', 'football', name='football'),
	url(r'^predictions/$', 'predictions', name='predictions'),
	url(r'^matches/$', 'matches', name='matches'),
)