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
    (r'^$', 'demo'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^demo/$', 'demo'),
    (r'^query/$', 'query_data'),
    (r'^tour/$', 'tour'),
    url(r'^comments/', include('django.contrib.comments.urls')), 
    url(r'^admin/django-lean/', include('sparrow.django_lean.experiments.admin_urls')),
    url(r'^django-lean/', include('sparrow.django_lean.experiments.urls')),
    url(r'^feedback/', include('sparrow.djangovoice.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.SITE_ROOT, "media/css"), 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.SITE_ROOT, "media/js"), 'show_indexes': True}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.SITE_ROOT, "media/images"), 'show_indexes': True}),
    )
