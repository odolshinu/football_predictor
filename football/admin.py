from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Level)
admin.site.register(Team)
admin.site.register(ChampionShip)
admin.site.register(Match)
admin.site.register(Prediction)
admin.site.register(League)
admin.site.register(UserLeague)
admin.site.register(Points)
admin.site.register(GameweekPoints)
admin.site.register(MatchPoints)
admin.site.register(ActiveGameweek)