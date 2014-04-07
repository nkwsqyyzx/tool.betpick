from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # 中体育
    url(r'^zso/$', 'app_odds.views.home', name='home'),
    url(r'^zso/(\d+)/$','app_odds.views.odds', name='odds'),
    # 捷豹比分网
    url(r'^nowscore/$','app_odds.views.nowscore_home',name='nowscore_home'),
    url(r'^nowscore/(\d+)/$','app_odds.views.nowscore', name='nowscore'),
    # amcharts license
    url(r'^amline/amcharts_key.txt$', RedirectView.as_view(url='/static/amline/amcharts_key.txt')),
)
