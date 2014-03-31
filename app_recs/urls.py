from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app_recs.views.home', name='home'),
    url(r'^best/$','app_recs.views.best', name='best'),
    url(r'^latest/$','app_recs.views.latest', name='latest'),
    url(r'^p/(.+)$','app_recs.views.person', name='person'),
)
