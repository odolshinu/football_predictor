from django.conf.urls import patterns, include, url

urlpatterns = patterns('authentication.views',
	url(r'^register/$', 'register', name='register'),
	url(r'^login/$', 'user_login', name='user_login'),
	url(r'^logout/$', 'user_logout', name='user_logout'),
	url(r'^forgot/password/$','send_password_reset_email', name='send_password_reset_email'),
)