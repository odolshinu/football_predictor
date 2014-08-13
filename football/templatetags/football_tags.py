import datetime
import pytz

from django import template

from football.models import UserLeague, Points

register = template.Library()

@register.filter
def match_started(prediction):
	if prediction.match.schedule > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
		return False
	return True

@register.filter
def subtractone(value):
	return int(value)-1

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
			if not prediction.match.stage:
				points += 5
			elif prediction.match.stage == 'F2':
				points += 30
			else:
				points += 20
		if prediction.score_status:
			if not prediction.match.stage:
				points += 10
			elif prediction.match.stage == 'F2':
				points += 50
			else:
				points += 30
		return points
	return 'NA'