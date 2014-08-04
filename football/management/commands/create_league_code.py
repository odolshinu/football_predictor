from django.core.management.base import BaseCommand

from football.models import League, ChampionShip

class Command(BaseCommand):
	def handle(self, *args, **options):
		worldcup = ChampionShip.objects.get(id=1)
		for league in League.objects.all():
			league.championship = worldcup
			league.save()