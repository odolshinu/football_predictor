import json

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.core import signing
from django.contrib.auth.models import User
from django.conf import settings

from .models import FavouriteTeam
from football.models import Team, UserLeague, League, Points
from utils.mandrill_helper import send_mail

# Create your views here.
def send_email(email, message, subject):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return 1

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

def send_password_reset_email(request):
    if request.POST.get('email',None):
        email = request.POST["email"]
        try:
            user = User.objects.get(username=email)
            token = signing.dumps(user.pk, salt=settings.PASSWORD_SALT)
            link = settings.SERVER_NAME + '/user/reset/'+token+'/'
            subject = "SoccerPredictor Password Reset"

            message = "Please go to this link {}. If you have any problems, don't hesitate to contact SoccerPredictor.in.".format(link,)

            m = send_email(user.username, message, subject)
            return HttpResponse(json.dumps({'success':True}))
        except:
            return HttpResponse(json.dumps({'success':False, 'err':'Invalid Email', 'err_msg':True}))
    else:
        return render_to_response('forgot_password.html', {}, context_instance=RequestContext(request))

def reset_password(request, token):
    if request.method == 'GET':
        token_expires = 3600 * 48
        try:
            user_pk = signing.loads(token, max_age=token_expires, salt=settings.PASSWORD_SALT)
            try:
                user = get_object_or_404(User, pk=user_pk)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return render_to_response('password_reset.html', {'token':token}, context_instance=RequestContext(request))
            except Http404:
                return HttpResponse("Unauthorized access")
        except signing.BadSignature:
            return HttpResponse("Unauthorized access")
    if request.user.is_authenticated():
        new_password = request.POST.get('new_pwd', None)
        if new_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(reverse('football'))
    else:
        return HttpResponse("Unauthorized access")