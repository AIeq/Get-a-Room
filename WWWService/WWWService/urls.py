from django.conf.urls import patterns, include, url
from django.contrib import admin
from WWWService.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'WWWService.views.search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^([A-Za-z0-9_-]+)/([A-Za-z0-9_-]*)$', 'WWWService.views.search'),
    url(r'^([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)/([\.\@A-Za-z0-9_-])+/([\,0-9_]+)$', 'WWWService.views.search'),
)
