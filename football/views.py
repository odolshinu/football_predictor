from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import UserLeague, Match

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
def predictions(request):
	return HttpResponse("predictions")
	# if request.method == 'GET':
	# 	matches = Match.objects.all()
	# 	return render_to_response('matches.html')

@login_required(login_url='/')
def matches(request):
	matches = Match.objects.all()
	return render_to_response('matches.html', {'matches':matches}, context_instance=RequestContext(request))