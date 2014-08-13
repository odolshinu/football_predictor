import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.http import Http404

# Create your models here.
class Level(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Team(models.Model):
	"""docstring for Team"""

	name = models.CharField(max_length=100)
	logo = models.ImageField(upload_to='logo', null=True, blank=True)
	level = models.ForeignKey(Level, null=True, blank=True)

	def __str__(self):
		return self.name


class ChampionShip(models.Model):
	"""docstring for ChampionShip"""

	name = models.CharField(max_length=100)
	season = models.CharField(max_length=7, null=True, blank=True)

	def __str__(self):
		return self.name
		

class Match(models.Model):
	"""docstring for Match"""

	ROUND_CHOICES = (
			('R16', 'Round of 16'),
			('R8', 'Quater Final'),
			('R4', 'Semi Final'),
			('L2', 'Losers Final'),
			('F2', 'Final'),
		)
		
	championship = models.ForeignKey(ChampionShip)
	home_team = models.ForeignKey(Team, related_name='home_team')
	away_team = models.ForeignKey(Team, related_name='away_team')
	winner = models.ForeignKey(Team, null=True, blank=True, related_name='winner')
	schedule = models.DateTimeField(null=True, blank=True)
	status = models.BooleanField(default=False)
	score = models.CharField(max_length=5, null=True, blank=True)
	stage = models.CharField(max_length=5, null=True, blank=True, choices=ROUND_CHOICES)
	gameweek = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return ' vs '.join([self.home_team.name, self.away_team.name])


class Prediction(models.Model):
	"""docstring for Prediction"""

	user = models.ForeignKey(User)
	match = models.ForeignKey(Match)
	prediction = models.ForeignKey(Team, null=True, blank=True)
	score= models.CharField(max_length=5, null=True, blank=True)
	prediction_status = models.BooleanField(default=False)
	score_status = models.BooleanField(default=False)

	def __str__(self):
		return ' : '.join([self.user.first_name, ' vs '.join([self.match.home_team.name, self.match.away_team.name])])


class League(models.Model):
	"""docstring for League"""

	def generate_code():
		return ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(8)])

	name = models.CharField(max_length=100)
	championship = models.ForeignKey(ChampionShip, null=True, blank=True)
	code = models.CharField(max_length=8, null=True, blank=True, default=generate_code)
	admin = models.ForeignKey(User, null=True, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		unique = False
		if not self.code:
			self.code = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(8)])
		while not unique:
			try:
				get_object_or_404(League, code=self.code)
				self.code = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(8)])
			except Http404:
				unique = True
		super(League, self).save(*args, **kwargs)


class UserLeague(models.Model):
	"""docstring for UserLeague"""
	
	user = models.ForeignKey(User)
	league = models.ForeignKey(League)

	def __str__(self):
		return ' : '.join([self.user.first_name, self.league.name])


class Points(models.Model):
	"""docstring for Points"""

	points = models.IntegerField(default=0)
	user_league = models.ForeignKey(UserLeague)

	def __str__(self):
		return ' : '.join([self.user_league.user.first_name, self.user_league.league.name])


class GameweekPoints(models.Model):
	"""docstring for GameweekPoints"""

	user_league = models.ForeignKey(UserLeague)
	points = models.IntegerField(default=0)
	gameweek = models.IntegerField(default=0)

	def __str__(self):
		return ' : '.join([self.user_league.user.first_name, self.user_league.league.name])


class MatchPoints(models.Model):
	"""docstring for MatchPoints"""

	user_league = models.ForeignKey(UserLeague)
	points = models.IntegerField(default=0)
	match = models.ForeignKey(Match)

	def __str__(self):
		return ' : '.join([self.user_league.user.first_name, self.user_league.league.name])

class ActiveGameweek(models.Model):
	gameweek = models.IntegerField()
	championship = models.ForeignKey(ChampionShip)

	def __str__(self):
		return self.championship.name
					
		
@receiver(post_save, sender=Team)
def create_team_fans_league(sender, *args, **kwargs):
	# print kwargs['instance']
	league = League(name=kwargs['instance'])
	league.save()

@receiver(post_save, sender=Match)
def save_match_result(sender, *args, **kwargs):
	match = kwargs['instance']
	if match.status:
		championship_leagues = League.objects.filter(championship=match.championship)
		predictions = Prediction.objects.filter(match=match)
		for prediction in predictions:
			if match.winner == prediction.prediction:
				prediction.prediction_status = True
			if match.score == prediction.score:
				prediction.score_status = True
			prediction.save()
			for user_league in prediction.user.userleague_set.filter(league__in=championship_leagues):
				for user_point in Points.objects.filter(user_league=user_league):
					user_point.points = calculate_point(match, prediction, user_point.points)
					user_point.save()
				gameweek_points_obj, created = GameweekPoints.objects.get_or_create(user_league=user_league, gameweek=match.gameweek)
				gameweek_points_obj.points = calculate_point(match, prediction, gameweek_points_obj.points)
				gameweek_points_obj.save()
				match_points_obj = MatchPoints(user_league=user_league, match=match)
				match_points_obj.points = calculate_point(match, prediction, 0)
				match_points_obj.save()

@receiver(post_save, sender=UserLeague)
def tie_userleague_points(sender, *args, **kwargs):
	user_league = kwargs['instance']
	league_point = Points(user_league=user_league)
	league_point.save()

def calculate_point(match, prediction, current_points):
	if prediction.prediction_status:
		if not match.stage:
			current_points += 5
		elif match.stage == 'F2':
			current_points += 30
		else:
			current_points += 20
	if prediction.score_status:
		if not match.stage:
			current_points += 10
		elif match.stage == 'F2':
			current_points += 50
		else:
			current_points += 30
	return current_points