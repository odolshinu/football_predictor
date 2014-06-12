from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .models import FavouriteTeam
from football.models import Team, UserLeague, League, Points

# Create your views here.
def register(request):
	if request.method == 'GET':
		teams = Team.objects.all()
		return render_to_response('register.html', {'teams':teams}, context_instance=RequestContext(request))
	username = request.POST['email']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username, email, password)
	user.first_name = request.POST['first_name']
	user.last_name = request.POST['last_name']
	user.save()
	favourite_team = FavouriteTeam()
	favourite_team.user = user
	favourite_team.team_id = request.POST['team']
	favourite_team.save()
	league = League.objects.get(name=favourite_team.team.name)
	user_league = UserLeague()
	user_league.user = user
	user_league.league = league
	user_league.save()
	# league_point = Points(user_league=user_league)
	# league_point.save()
	return HttpResponseRedirect(reverse('home'))

def user_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
		else:
			return HttpResponse('User is not active')
	else:
		return HttpResponse('The email/password combination you tried is invalid')
	return HttpResponseRedirect(reverse('football'))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))