import datetime

from django import template

from football.models import UserLeague, Points

register = template.Library()

@register.filter
def match_started(match):
	if match.schedule > datetime.datetime.now:
		return False
	return True

@register.simple_tag
def get_points(league):
	return league.points_set.all()[0].points

@register.simple_tag
def get_rank(user_league):
	# league = League.objects.get(id=id)
	league_users = UserLeague.objects.filter(league=user_league.league)
	league_users_points = Points.objects.filter(user_league__in=league_users).order_by('-points')
	league_user_point = Points.objects.get(user_league=user_league)
	return list(league_users_points).index(league_user_point)+1

@register.simple_tag
def get_prediction_points(prediction):
	if prediction.match.status:
		points = 0
		if prediction.prediction_status:
			points += 10
		if prediction.score_status:
			points += 20
		return points
	return 'NA'