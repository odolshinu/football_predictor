from django.db import models
from django.contrib.auth.models import User

from football.models import Team

# Create your models here.
class FavouriteTeam(models.Model):
	"""docstring for FavouriteTeam"""

	user = models.ForeignKey(User)
	team = models.ForeignKey(Team)
	
	def __str__(self):
		return ' : '.join([self.user.first_name, self.team.name])