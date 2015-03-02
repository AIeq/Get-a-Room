from django.conf.urls import patterns, include, url
from WWWService.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
      url(r"^$", 'WWWService.views.search'),
    # static version:
    # url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    # Examples:
    # url(r'^$', 'WWWService.views.home', name='home'),
    # url(r'^WWWService/', include('WWWService.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
