from django.conf import settings

from football.models import Level, Team

def teams(request):
	club_level = Level.objects.get(name='Club')
	club_teams = Team.objects.filter(level=club_level).order_by('name')
	return {'club_teams':club_teams}

def logo_url(request):
	return {'LOGO_URL':settings.LOGO_URL}