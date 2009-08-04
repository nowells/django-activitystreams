from django.conf.urls.defaults import patterns, url, include, handler500, handler404

urlpatterns = patterns('',
    (r'', include('activitystreams.urls')),
)
