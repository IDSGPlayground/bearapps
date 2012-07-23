from django.conf.urls.defaults import patterns, include, url

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
      url(r'^admin/', include(admin.site.urls)),
      url(r'^register', 'store.views.register', name='register'),
      url(r'^browse/', 'store.views.browse', name='browse' ),
      url(r'^my-apps/', 'store.views.myapps', name='my-apps'),
      url(r'^manage/', 'store.views.manage', name='manage'),
)
