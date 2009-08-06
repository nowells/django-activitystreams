from django.conf.urls.defaults import patterns, url, include, handler500, handler404
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from activitystreams.handlers import GlobalActivityHandler, SourceActivityHandler, SourceActionHandler, GlobalActionHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

source_activity_resource = Resource(handler=SourceActivityHandler, **ad)
global_activity_resource = Resource(handler=GlobalActivityHandler, **ad)

global_action_resource = Resource(handler=GlobalActionHandler, **ad)
source_action_resource = Resource(handler=SourceActionHandler, **ad)

urlpatterns = patterns('',
    # Global Activities
    url(r'^activities\.(?P<emitter_format>.+)$', global_activity_resource),
    url(r'^activity/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', global_activity_resource),

    # Source-Specific Activities
    url(r'^(?P<source>[\w\-_]+)/activities\.(?P<emitter_format>.+)$', source_activity_resource),
    url(r'^(?P<source>[\w\-_]+)/activity/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', source_activity_resource),

    #Global Actions
    url(r'^actions\.(?P<emitter_format>.+)$', global_action_resource),
    url(r'^action/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', global_action_resource),

    # Source-Specific Actions
    url(r'^(?P<source>[\w\-_]+)/actions\.(?P<emitter_format>.+)$', source_action_resource),
    url(r'^(?P<source>[\w\-_]+)/action/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', source_action_resource),
)
