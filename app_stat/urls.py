from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # 统计网站主入口
    url(r'^$', 'app_stat.views.stat_home', name='stat_home'),
    # Simple soccer states
    url(r'^l/$', 'app_stat.views.stat_league', name='stat_league'),
    url(r'^l/(\d+)&n=(.+)/$', 'app_stat.views.stat_league_matches', name='stat_league_matches'),
    url(r'^l/u=(.+)&h=(.+)&a=(.+)/$', 'app_stat.views.stat_match', name='stat_match'),
    # WhoScored
    # 支持统计数据的联赛列表
    url(r'^w/$', 'app_stat.views.w_stat_league', name='w_stat_league'),
    # 联赛中的比赛列表
    url(r'^w/lm/(.+)/(.+)/$', 'app_stat.views.w_stat_league_matches', name='w_stat_league_matches'),
    # 两支球队的统计数据列表
    url(r'^w/ms/(.+)/(.+)/(.+)/(.+)/$', 'app_stat.views.w_stat_match', name='w_stat_match'),
)
