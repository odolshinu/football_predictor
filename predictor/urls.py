from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'predictor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'football.views.home', name='home'),
    url(r'^user/', include('authentication.urls')),
    url(r'^football/', include('football.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
