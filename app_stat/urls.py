from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # simplesoccerstats
    url(r'^$','app_stat.views.stat_home',name='stat_home'),
    url(r'^l/$','app_stat.views.stat_league',name='stat_league'),
    url(r'^l/(\d+)/$','app_stat.views.stat_league_matches',name='stat_league_matches'),
    url(r'^/(\d+)$','app_stat.views.stat_match', name='stat_match'),
)
