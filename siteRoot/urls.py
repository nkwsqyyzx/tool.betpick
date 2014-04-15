from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.siteRoot.urls)),
    # 赔率
    url(r'^odds/', include('app_odds.urls')),
    # 推荐
    url(r'^recs/', include('app_recs.urls')),
    # 统计
    url(r'^stat/', include('app_stat.urls')),
)
