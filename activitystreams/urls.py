from django.conf.urls.defaults import patterns, url, include, handler500, handler404
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from activitystreams.handlers import ActivityHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

activity_resource = Resource(handler=ActivityHandler, **ad)

urlpatterns = patterns('',
    url(r'^activities\.(?P<emitter_format>.+)$', activity_resource),
    url(r'^activity/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', activity_resource),
)
