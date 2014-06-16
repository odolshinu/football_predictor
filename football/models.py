from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Team(models.Model):
	"""docstring for Team"""

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class ChampionShip(models.Model):
	"""docstring for ChampionShip"""

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
		

class Match(models.Model):
	"""docstring for Match"""
		
	championship = models.ForeignKey(ChampionShip)
	home_team = models.ForeignKey(Team, related_name='home_team')
	away_team = models.ForeignKey(Team, related_name='away_team')
	winner = models.ForeignKey(Team, null=True, blank=True, related_name='winner')
	schedule = models.DateTimeField(null=True, blank=True)
	status = models.BooleanField(default=False)
	score = models.CharField(max_length=5, null=True, blank=True)

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

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


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

@receiver(post_save, sender=Team)
def create_team_fans_league(sender, *args, **kwargs):
	# print kwargs['instance']
	league = League(name=kwargs['instance'])
	league.save()

@receiver(post_save, sender=Match)
def save_match_result(sender, *args, **kwargs):
	match = kwargs['instance']
	if match.status:
		predictions = Prediction.objects.filter(match=match)
		for prediction in predictions:
			if match.winner == prediction.prediction:
				prediction.prediction_status = True
			if match.score == prediction.score:
				prediction.score_status = True
			prediction.save()
			for user_league in prediction.user.userleague_set.all():
				for user_point in Points.objects.filter(user_league=user_league):
					if prediction.prediction_status:
						user_point.points += 10
					if prediction.score_status:
						user_point.points += 20
					user_point.save()

@receiver(post_save, sender=UserLeague)
def tie_userleague_points(sender, *args, **kwargs):
	user_league = kwargs['instance']
	league_point = Points(user_league=user_league)
	league_point.save()