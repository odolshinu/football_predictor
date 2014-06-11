import datetime

from django import template

# from .models import Match

register = template.Library()

@register.filter
def match_started(match):
	if match.schedule > datetime.datetime.now:
		return False
	return True