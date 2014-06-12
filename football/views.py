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
	return render_to_response('home.html', {}, context_instance=RequestContext(request))

@login_required(login_url='/')
def football(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	leagues = UserLeague.objects.filter(user=request.user)
	return render_to_response('football_home.html',
								{
									'full_name':full_name,
									'leagues':leagues,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def my_predictions(request):
	if request.method == 'POST':
		prediction = Prediction()
		match = Match.objects.get(id=request.POST['match'])
		prediction.match = match
		prediction.user = request.user
		# if request.POST['winner']:
		# 	prediction.prediction_id = request.POST['winner']
		home_score = request.POST.get('home', 0)
		away_score = request.POST.get('away', 0)
		prediction.score = '-'.join([str(home_score), str(away_score)])
		if home_score > away_score:
			prediction.prediction = match.home_team
		elif home_score < away_score:
			prediction.prediction = match.away_team
		prediction.save()
	predictions = Prediction.objects.filter(user=request.user)
	predicted_matches = [prediction.match for prediction in predictions]
	matches = Match.objects.filter(schedule__gt=datetime.datetime.now())
	upcoming_matches = set(matches).difference(set(predicted_matches))
	return render_to_response('my_predictions.html',
								{
									'predictions':predictions,
									'upcoming_matches':upcoming_matches,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def matches(request):
	matches = Match.objects.all()
	return render_to_response('matches.html', {'matches':matches}, context_instance=RequestContext(request))

@login_required(login_url='/')
def league(request, id=None):
	league = League.objects.get(id=id)
	user_leagues = UserLeague.objects.filter(league=league)
	user_points = Points.objects.filter(user_league__in=user_leagues).order_by('-points')
	return render_to_response('league.html',
								{
									'user_points':user_points,
									'league':league,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def predictions(request, id=None):
	if int(id) == request.user.id:
		return HttpResponseRedirect(reverse('my_predictions'))
	user = User.objects.get(id=id)
	predictions = Prediction.objects.filter(user=user)
	return render_to_response('predictions.html',
								{
									'user':user,
									'predictions':predictions,
								},
							context_instance=RequestContext(request))