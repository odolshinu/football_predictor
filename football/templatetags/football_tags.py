import datetime

from django import template

# from .models import Match

register = template.Library()

@register.filter
def match_started(match):
	if match.schedule > datetime.datetime.now:
		return False
	return True

@register.simple_tag
def get_points(league):
	return league.points_set.all()[0].points