import datetime

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import UserLeague, Match, Prediction, League, Points

# Create your views here.

def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('football'))
	return render_to_response('home.html', {}, context_instance=RequestContext(request))

@login_required(login_url='/')
def football(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	leagues = UserLeague.objects.filter(user=request.user)
	last_three_matches = Match.objects.filter(status=True).order_by('-schedule')[:3]
	upcoming_matches = Match.objects.filter(schedule__gt=datetime.datetime.now())[:3]
	return render_to_response('football_home.html',
								{
									'full_name':full_name,
									'leagues':leagues,
									'last_three_matches':last_three_matches,
									'upcoming_matches':upcoming_matches,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def my_predictions(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	if request.method == 'POST':
		prediction = Prediction()
		match = Match.objects.get(id=request.POST['match'])
		prediction.match = match
		prediction.user = request.user
		# if request.POST['winner']:
		# 	prediction.prediction_id = request.POST['winner']
		home_score = 0
		away_score = 0
		if request.POST.get('home', None):
			home_score = request.POST['home']
			if not str(home_score).isdigit():
				home_score = 0
		if request.POST.get('away', None):
			away_score = request.POST['away']
			if not str(away_score).isdigit():
				away_score = 0
		prediction.score = '-'.join([str(home_score), str(away_score)])
		if home_score > away_score:
			prediction.prediction = match.home_team
		elif home_score < away_score:
			prediction.prediction = match.away_team
		prediction.save()
		return HttpResponseRedirect(reverse('my_predictions'))
	predictions = Prediction.objects.filter(user=request.user)
	predicted_matches = [prediction.match for prediction in predictions]
	matches = Match.objects.filter(schedule__gt=datetime.datetime.now()).order_by('schedule')
	upcoming_matches = set(matches).difference(set(predicted_matches))
	upcoming = sorted(list(upcoming_matches), key=lambda x:x.schedule)
	return render_to_response('my_predictions.html',
								{
									'full_name':full_name,
									'predictions':predictions,
									'upcoming_matches':upcoming,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def matches(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	matches = Match.objects.all().order_by('schedule')
	return render_to_response('matches.html', {'matches':matches,'full_name':full_name,}, context_instance=RequestContext(request))

@login_required(login_url='/')
def league(request, id=None):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	league = League.objects.get(id=id)
	user_leagues = UserLeague.objects.filter(league=league)
	user_points = Points.objects.filter(user_league__in=user_leagues).order_by('-points')
	users_in_league = [ user_league.user for user_league in user_leagues ]
	next_matches = Match.objects.filter(schedule__gt=datetime.datetime.now()).order_by('schedule')
	if next_matches:
		next_match = next_matches[0]
		next_match_predictions = next_match.prediction_set.filter(user__in=users_in_league)
	else:
		next_match_predictions = []
		next_match = None
	return render_to_response('league.html',
								{
									'full_name':full_name,
									'user_points':user_points,
									'league':league,
									'next_match_predictions':next_match_predictions,
									'next_match':next_match,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def predictions(request, id=None):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	if int(id) == request.user.id:
		return HttpResponseRedirect(reverse('my_predictions'))
	prediction_user = User.objects.get(id=id)
	predictions = Prediction.objects.filter(user=prediction_user)
	return render_to_response('predictions.html',
								{
									'full_name':full_name,
									'prediction_user':prediction_user,
									'predictions':predictions,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def leagues(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	user_leagues = UserLeague.objects.filter(user=request.user)
	return render_to_response('leagues.html',
								{
									'full_name':full_name,
									'user_leagues':user_leagues,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def standings(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	user_leagues = UserLeague.objects.filter(user=request.user)
	league_points = Points.objects.filter(user_league__in=user_leagues)
	return render_to_response('standings.html',
								{
									'league_points':league_points,
									'full_name':full_name,
								},
							context_instance=RequestContext(request))