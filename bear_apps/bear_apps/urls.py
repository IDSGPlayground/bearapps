from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
from store.api import UserResource, AppResource, ChartResource, GroupResource

dajaxice_autodiscover()
user_resource = UserResource()
group_resource = GroupResource()
chart_resource = ChartResource()
app_resource = AppResource()

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
      url(r'^classselect', 'store.views.classselect', name='classselect'),
      url(r'^browse/', 'store.views.browse', name='browse'),
      url(r'^my-apps/', 'store.views.myapps', name='my-apps'),
      url(r'^manage/', 'store.views.manage', name='manage'),
      url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
      url(r'^api/', include(user_resource.urls)),
      url(r'^api/', include(app_resource.urls)),
      url(r'^api/', include(group_resource.urls)),
      url(r'^api/', include(chart_resource.urls)),
)
