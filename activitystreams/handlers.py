"""
Handlers for the Django-Activitystreams REST API.
"""

import re
import datetime

from piston.handler import BaseHandler
from piston.utils import rc, throttle, require_extended

from activitystreams.models import Activity, Action, Source, ActivityObject

class SourceActivityHandler(BaseHandler):
    """
    The primary handler for the system, this handles creating Activity records, as well as all associated records.
    """
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST',)
    fields = ('content', ('user', ('username', 'first_name')), 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Activity

    @require_extended
    def create(self, request, source_name):
        """
        Creates a new Activity record.

        :param action_slug: The slug for the Action that this Activity is related to.
        :type action_slug: String
        :param user_id: The User ID for the User associated with this Action TODO: Figure out how to handle users
        :type user_id: TBD
        :param direct_object_content_type_id: ContentType ID for the direct object of this Activity.
        :type direct_object_content_type_id: Integer
        :param direct_object_object_id: Object ID for the direct object of this Activity.
        :type direct_object_object_id: Integer
        :param indirect_object_content_type_id: ContentType ID for the indirect object of this Activity.
        :type indirect_object_content_type_id: Integer
        :param indirect_object_object_id: Object ID for the indirect object of this Activity.
        :type indirect_object_object_id: Integer
        """
        if self.exists(content=request.data['content'], user__id=request.data['user_id']):
            return rc.DUPLICATE_ENTRY
        else:
            source = Source.objects.get(name=source_name)
            action = Action.objects.get(source=source, slug=request.data['action_slug'])

            if request.data.get('direct_object_content_type_id', None) and request.data.get('direct_object_object_id', None):
                direct_object, created = ActivityObject.objects.get_or_create(
                    source = source,
                    content_type_id = request.data['direct_object_content_type_id'],
                    object_id = request.data['direct_object_object_id'],
                )
            else:
                direct_object = None

            if request.data.get('indirect_object_content_type_id', None) and request.data.get('indirect_object_object_id', None):
                indirect_object, created = ActivityObject.objects.get_or_create(
                    source = source,
                    content_type_id = request.data['indirect_object_content_type_id'],
                    object_id = request.data['indirect_object_object_id'],
                )
            else:
                indirect_object = None

            activity = Activity(
                action = action,
                user_id = request.data.get('user_id', ''),
                direct_object = direct_object,
                indirect_object = indirect_object,
                timestamp = request.data.get('timestamp', datetime.datetime.now()),
                extra_data = request.data.get('extra_data', None),
                content=request.data.get('content', ''),
            )
            activity.save()

            return activity

    def read(self, request, source_name, id=None):
        if id is not None:
            activity = Activity.objects.get(pk=id, action__source__name=source_name)
        else:
            activity = Activity.objects.filter(action__source__name=source_name) #TODO: Don't return huge lists of stuff.
        return activity

    @throttle(5, 10 * 60) # allow 5 times in 10 minutes
    def update(self, request, id, source_name):
        activity = Activity.objects.get(pk=id, action__source__name=source_name)
        activity.timestamp = request.PUT.get('timestamp')
        activity.save()
        return activity

    def delete(self, request, id, source_name):
        activity = Activity.objects.get(pk=id, action__source__name=source_name)

        if not request.user == activity.user:
            return rc.FORBIDDEN # returns HTTP 401

        activity.delete()

        return rc.DELETED # returns HTTP 204

class GlobalActivityHandler(BaseHandler):
    """
    The primary handler for the global activity on the system, this only allows reading of content.
    """
    allowed_methods = ('GET',)
    fields = ('content', ('user', ('username', 'first_name')), 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Activity

    def read(self, request, id=None):
        if id is not None:
            activity = Activity.objects.get(pk=id)
        else:
            activity = Activity.objects.all() #TODO: Don't return huge lists of stuff.
        return activity

class SourceActionHandler(BaseHandler):
    """
    The primary handler for the system, this handles creating Activity records, as well as all associated records.
    """
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST',)
    fields = ('slug', ('source', ('name',)), 'template', 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Action

    @require_extended
    def create(self, request, source_name):
        """
        Creates a new Action record.

        :param source_name: The pre-registered Source name for this Action to be attached to
        :type source_name: String
        :param action_slug: The slug for the Action that this Activity is related to.
        :type action_slug: String
        :param action_template: The Django template snippet for rendering this Action
        :type action_template: String
        """
        if self.exists(slug=request.data['action_slug'], source__name=source_name):
            return rc.DUPLICATE_ENTRY
        else:
            source = Source.objects.get(name=source_name)
            action = Action.objects.get(
                source = source,
                slug = request.data['action_slug'],
                template = request.data['action_template'],
            )
            action.save()

            return action

    def read(self, request, source_name, id=None):
        if id is not None:
            action = Action.objects.get(pk=id, source__name=source_name)
        else:
            action = Action.objects.filter(source__name=source_name) #TODO: Don't return huge lists of stuff.
        return action

    @throttle(5, 10 * 60) # allow 5 times in 10 minutes
    def update(self, request, id, source_name):
        """
        Updates an Action record.

        :param source_name: The pre-registered Source name for this Action to be attached to
        :type source_name: String
        :param action_slug: The slug for the Action that this Activity is related to.
        :type action_slug: String
        :param action_template: The Django template snippet for rendering this Action
        :type action_template: String
        """
        action = Action.objects.get(pk=id, source__name=source_name)
        action.slug = request.PUT.get('action_slug')
        action.template = request.PUT.get('action_template')
        action.save()
        return action

    def delete(self, request, id, source_name):
        action = Action.objects.get(pk=id, source__name=source_name)

        if not request.user == activity.user:
            return rc.FORBIDDEN # returns HTTP 401

        action.delete()

        return rc.DELETED # returns HTTP 204

class GlobalActionHandler(BaseHandler):
    """
    Allows reading of all Actions.
    """
    allowed_methods = ('GET',)
    fields = ('slug', ('source', ('name',)), 'template', 'resource_uri')
    #exclude = ('id', re.compile(r'^private_'))
    model = Action

    def read(self, request, id=None):
        if id is not None:
            action = Action.objects.get(pk=id)
        else:
            action = Action.objects.all() #TODO: Don't return huge lists of stuff.
        return action
