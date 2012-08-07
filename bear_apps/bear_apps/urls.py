from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'store.views.home', name='home'),
    # url(r'^bear_apps/', include('bear_apps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^backend/', include(admin.site.urls)),
      url(r'^admin/', 'store.views.admin', name='admin'),
      url(r'^register', 'store.views.register', name='register'),
      url(r'^browse/', 'store.views.browse', name='browse'),
      url(r'^my-apps/', 'store.views.myapps', name='my-apps'),
      url(r'^manage/', 'store.views.manage', name='manage'),
      url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
