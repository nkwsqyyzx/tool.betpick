from django.conf.urls import patterns, include, url

from django.contrib import admin
from betpick.views import odds
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'betpick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\d+)/$', odds),
)
