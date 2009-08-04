import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from activitystreams.models import Activity

class ActivityHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('title', 'content', ('author', ('username', 'first_name')), 'content_size')
    exclude = ('id', re.compile(r'^private_'))
    model = Activity

    @classmethod
    def content_size(cls, activity):
        return len(activity.content)

    def read(self, request, id):
        activity = Activity.objects.get(pk=id)
        return activity

    @throttle(5, 10 * 60) # allow 5 times in 10 minutes
    def update(self, request, id):
        activity = Activity.objects.get(pk=id)
        activity.timestamp = request.PUT.get('timestamp'))
        activity.save()
        return activity

    def delete(self, request, id):
        activity = Activity.objects.get(pk=id)

        if not request.user == activity.user:
            return rc.FORBIDDEN # returns HTTP 401

        activity.delete()

        return rc.DELETED # returns HTTP 204
