import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from activitystreams.models import Activity

class ActivityListHandler(BaseHandler):
    allowed_methods = ('GET',)
    #fields = ('content', 'resource_uri',)

    def read(self, request):
        return Activity.objects.all()

class ActivityHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('content', ('user', ('username', 'first_name')), 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Activity

    def read(self, request, id):
        activity = Activity.objects.get(pk=id)
        return activity

    @throttle(5, 10 * 60) # allow 5 times in 10 minutes
    def update(self, request, id):
        activity = Activity.objects.get(pk=id)
        activity.timestamp = request.PUT.get('timestamp')
        activity.save()
        return activity

    def delete(self, request, id):
        activity = Activity.objects.get(pk=id)

        if not request.user == activity.user:
            return rc.FORBIDDEN # returns HTTP 401

        activity.delete()

        return rc.DELETED # returns HTTP 204
