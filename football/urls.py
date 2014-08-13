from django.conf.urls import patterns, include, url

urlpatterns = patterns('football.views',
	url(r'^$', 'football', name='football'),
	url(r'^my/predictions/$', 'my_predictions', name='my_predictions'),
	url(r'^matches/$', 'matches', name='matches'),
	url(r'^(?P<gameweek>\d+)/matches/$', 'matches', name='other_matches'),
	url(r'^leagues/$', 'leagues', name='leagues'),
	url(r'^(?P<id>\d+)/league/$', 'league', name='league'),
	url(r'^(?P<id>\d+)/predictions/$', 'predictions', name='predictions'),
	url(r'^standings/$', 'standings', name='standings'),
	url(r'^create/league/$', 'create_league', name='create_league'),
	url(r'^join/league/$', 'join_league', name='join_league'),
	url(r'^add/favourite/team/$', 'add_favourite_team', name='add_favourite_team'),
	url(r'^(?P<id>\d+)/league/history/$', 'league_history', name='league_history'),
)