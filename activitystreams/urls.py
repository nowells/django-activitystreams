from django.conf.urls.defaults import patterns, url, include, handler500, handler404
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from activitystreams.handlers import ActivityHandler, ActivityListHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

activity_resource = Resource(handler=ActivityHandler, **ad)
activity_list_resource = Resource(handler=ActivityListHandler, **ad)

urlpatterns = patterns('',
    url(r'^activity\.(?P<emitter_format>.+)$', activity_list_resource),
    url(r'^activity/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', activity_resource),
)
