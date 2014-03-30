from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.siteRoot.urls)),
    url(r'^odds/', include('app_odds.urls')),
    url(r'^recs/', include('app_recs.urls')),
)
