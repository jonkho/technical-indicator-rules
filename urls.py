from django.conf.urls.defaults import *
import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sparrow.webapp.views',
    # Example:
    # (r'^sparrow/', include('sparrow.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'login'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^demo/$', 'demo'),
    (r'^ticker/$', 'ticker_data'),
    (r'^indicator/$', 'indicator_data'),
    (r'^query/$', 'query_data'),
    (r'^chart/$', 'chart'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.SITE_ROOT, "media/css"), 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.SITE_ROOT, "media/js"), 'show_indexes': True}),
    )
