import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle, require_extended

from activitystreams.models import Activity, Action

class ActivityHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST',)
    fields = ('content', ('user', ('username', 'first_name')), 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Activity

    def read(self, request, id=None):
        if id is not None:
            activity = Activity.objects.get(pk=id)
        else:
            activity = Activity.objects.all() #TODO: Don't return huge lists of stuff.
        return activity

    #@throttle(5, 10 * 60) # allow 5 times in 10 minutes
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

    @require_extended
    def create(self, request):
        """
        Creates a new Activity record.
        """
        if self.exists(content=request.data['content']):
            return rc.DUPLICATE_ENTRY
        else:
            activity = Activity(action_id=1,
                            content=request.data['content'],
                            user=request.user)
            activity.save()

            return activity
