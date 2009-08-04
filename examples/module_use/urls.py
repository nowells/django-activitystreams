import os

import django
from django.conf.urls.defaults import patterns, url, include, handler500, handler404
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

django_admin_media_path = os.path.join(os.path.abspath(os.path.dirname(django.__file__)), 'contrib', 'admin', 'media')

urlpatterns = patterns('',
    url(r'^api/', include('activitystreams.urls')),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^django-admin-media/(?P<path>.*)$', serve, {'document_root': django_admin_media_path}),
)
