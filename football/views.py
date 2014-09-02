import datetime
import pytz

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from .models import UserLeague, Match, Prediction, League, Points, ChampionShip, Team, \
					GameweekPoints, ActiveGameweek, MatchPoints, Level

from authentication.models import FavouriteTeam

# Create your views here.

def home(request):
	# if request.user.is_authenticated():
	# 	return HttpResponseRedirect(reverse('football'))
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	active_gameweek = ActiveGameweek.objects.get(championship=championship).gameweek
	results = Match.objects.filter(championship=championship, status=True, gameweek=active_gameweek-1)
	matches = Match.objects.filter(championship=championship, gameweek=active_gameweek)
	club_level = Level.objects.get(name='Club')
	club_teams = Team.objects.filter(level=club_level).order_by('name')
	return render_to_response('football/home.html',
								{
									'results':results,
									'LOGO_URL':settings.LOGO_URL,
									'matches':matches,
									'club_teams':club_teams,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def football(request):
	# leagues = UserLeague.objects.filter(user=request.user)
	# last_three_matches = Match.objects.filter(status=True).order_by('-schedule')[:3]
	# upcoming_matches = Match.objects.filter(schedule__gt=datetime.datetime.now())[:3]
	gameweek_match_points = []
	active_gameweek = 0
	current_season_club_added = False
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	current_championship_automatic_leagues = League.objects.filter(admin=None, championship=championship)
	user_leagues = UserLeague.objects.filter(user=request.user, league__in=current_championship_automatic_leagues)
	club_level = Level.objects.get(name='Club')
	club_teams = Team.objects.filter(level=club_level).order_by('name')
	if user_leagues:
		current_season_club_added = True
	if current_season_club_added:
		active_gameweek = ActiveGameweek.objects.get(championship=championship).gameweek
		gameweek_points = GameweekPoints.objects.filter(user_league=user_leagues[0], gameweek=active_gameweek-1)
		if gameweek_points:
			gameweek_matches = Match.objects.filter(championship=championship, gameweek=active_gameweek-1)
			gameweek_match_points = MatchPoints.objects.filter(user_league=user_leagues[0], match__in=gameweek_matches)
		else:
			return HttpResponseRedirect(reverse('my_predictions'))
	return render_to_response('football/points.html',
								{
									'current_championship_automatic_leagues':current_championship_automatic_leagues,
									'current_season_club_added':current_season_club_added,
									'gameweek_match_points':gameweek_match_points,
									'gameweek':active_gameweek-1,
									'championship':championship,
									'LOGO_URL':settings.LOGO_URL,
									'club_teams':club_teams,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def my_predictions(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	if request.method == 'POST':
		if request.POST.get('prediction', None):
			prediction = Prediction.objects.get(id=request.POST['prediction'])
			match = prediction.match
		else:
			match = Match.objects.get(id=request.POST['match'])
		if match.schedule > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
			if not request.POST.get('prediction', None):
				try:
					prediction = get_object_or_404(Prediction, match=match, user=request.user)
				except Http404:
					prediction = Prediction()
					prediction.match = match
					prediction.user = request.user
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
			else:
				prediction.prediction = None
			prediction.save()
		return HttpResponseRedirect(reverse('my_predictions'))
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	active_gameweek = ActiveGameweek.objects.get(championship=championship)
	gameweek_matches = Match.objects.filter(championship=championship, gameweek=active_gameweek.gameweek)
	predictions = Prediction.objects.filter(user=request.user, match__in=gameweek_matches).order_by('-id')
	predicted_matches = [prediction.match for prediction in predictions]
	matches = Match.objects.filter(schedule__gt=datetime.datetime.now(), championship=championship).order_by('schedule')
	upcoming_matches = set(matches).difference(set(predicted_matches))
	upcoming = sorted(list(upcoming_matches), key=lambda x:x.schedule)
	return render_to_response('my_predictions.html',
								{
									'full_name':full_name,
									'predictions':predictions,
									'upcoming_matches':upcoming,
								},
							context_instance=RequestContext(request))

def matches(request, gameweek=None):
	# full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	active_gameweek = ActiveGameweek.objects.get(championship=championship).gameweek
	if not gameweek:
		gameweek = active_gameweek
	matches = Match.objects.filter(championship=championship, gameweek=gameweek).order_by('schedule')
	club_level = Level.objects.get(name='Club')
	club_teams = Team.objects.filter(level=club_level).order_by('name')
	return render_to_response('football/matches.html',
								{
									'matches':matches,
									# 'full_name':full_name,
									'gameweek':int(gameweek),
									'championship':championship,
									'active_gameweek':active_gameweek,
									'LOGO_URL':settings.LOGO_URL,
									'club_teams':club_teams,
								}, context_instance=RequestContext(request))

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
	predictions = Prediction.objects.filter(user=prediction_user).order_by('-id')
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
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	leagues = League.objects.filter(championship=championship)
	user_leagues = UserLeague.objects.filter(user=request.user, league__in=leagues)
	championships = ChampionShip.objects.all()
	return render_to_response('leagues.html',
								{
									'full_name':full_name,
									'user_leagues':user_leagues,
									'championships':championships,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def standings(request):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	leagues = League.objects.filter(championship=championship)
	user_leagues = UserLeague.objects.filter(user=request.user, league__in=leagues)
	league_points = Points.objects.filter(user_league__in=user_leagues)
	return render_to_response('standings.html',
								{
									'league_points':league_points,
									'full_name':full_name,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def create_league(request):
	championship = ChampionShip.objects.get(id=request.POST['championship'])
	league = League()
	league.championship = championship
	league.admin = request.user
	league.name = request.POST['league_name']
	league.save()
	user_league = UserLeague()
	user_league.league = league
	user_league.user = request.user
	user_league.save()
	return HttpResponseRedirect(reverse('leagues'))

@login_required(login_url='/')
def join_league(request):
	league = League.objects.get(code=request.POST['code'])
	user_league = UserLeague()
	user_league.league = league
	user_league.user = request.user
	user_league.save()
	return HttpResponseRedirect(reverse('leagues'))

@login_required(login_url='/')
def add_favourite_team(request):
	league = League.objects.get(code=request.POST['code'])
	user_league = UserLeague()
	user_league.league = league
	user_league.user = request.user
	user_league.save()
	team = Team.objects.get(name=league.name)
	favourite_team = FavouriteTeam(team=team, user=request.user)
	favourite_team.save()
	return HttpResponseRedirect(reverse('football'))

@login_required(login_url='/')
def league_history(request, id):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	user_league = UserLeague.objects.get(id=id)
	gameweek_points = GameweekPoints.objects.filter(user_league=user_league)
	return render_to_response('gameweek_history.html',
								{
									'gameweek_points':gameweek_points,
									'full_name':full_name,
									'user_league':user_league,
								},
							context_instance=RequestContext(request))

@login_required(login_url='/')
def gameweek_details(request, ul_id, gw_id):
	full_name = ' '.join([request.user.first_name.capitalize(), request.user.last_name.capitalize()])
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	user_league = UserLeague.objects.get(id=ul_id)
	matches = Match.objects.filter(championship=championship, gameweek=gw_id)
	match_points = MatchPoints.objects.filter(user_league_id=ul_id, match__in=matches)
	return render_to_response('gameweek_details.html',
								{
									'match_points':match_points,
									'full_name':full_name,
									'gameweek':gw_id,
									'user_league':user_league
								},
							context_instance=RequestContext(request))

def design(request):
	championship = ChampionShip.objects.get(name="English Premier League", season="2014-15")
	active_gameweek = ActiveGameweek.objects.get(championship=championship).gameweek
	results = Match.objects.filter(championship=championship, status=True, gameweek=active_gameweek-1)
	matches = Match.objects.filter(championship=championship, gameweek=active_gameweek)
	club_level = Level.objects.get(name='Club')
	club_teams = Team.objects.filter(level=club_level).order_by('name')
	return render_to_response('design.html',
								{
									'results':results,
									'LOGO_URL':settings.LOGO_URL,
									'matches':matches,
									'club_teams':club_teams,
								},
							context_instance=RequestContext(request))