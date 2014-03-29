from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from siteRoot.views import odds,home

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.siteRoot.urls)),
    url(r'^$', 'siteRoot.views.home', name='home'),
    url(r'^(\d+)/$', odds),
    url(r'^amline/amcharts_key.txt$', RedirectView.as_view(url='/static/amline/amcharts_key.txt')),
)
