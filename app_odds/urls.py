from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app_odds.views.home', name='home'),
    url(r'^(\d+)/$','app_odds.views.odds', name='odds'),
    url(r'^amline/amcharts_key.txt$', RedirectView.as_view(url='/static/amline/amcharts_key.txt')),
)
