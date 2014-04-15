from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # simplesoccerstats
    url(r'^$','app_stat.views.stat_home',name='stat_home'),
    url(r'^/(\d+)$','app_stat.views.stat_match', name='stat_match'),
)
