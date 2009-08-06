import datetime

from activitystreams import settings
from django.contrib.contenttypes.models import ContentType
from wellrested import JsonRestClient

class ActivityStream(object):
    def __init__(self):
        self._client = JsonRestClient(settings.ACTIVITYSTREAMS_BASE_URL, settings.ACTIVITYSTREAMS_USERNAME, settings.ACTIVITYSTREAMS_PASSWORD)

    def record_activity(self, action_slug=None, user_id=None, direct_object=None, indirect_object=None, timestamp=None, context=None):
        try:
            if timestamp is None:
                timestamp = datetime.datetime.now()

            response = self._client.post(
                '%s/activities.json' % settings.ACTIVITYSTREAMS_SOURCE,
                data={
                    'action': action_slug,
                    'user_id': user_id,
                    'direct_object_content_type_id': direct_object and ContentType.objects.get_for_model(direct_object).id or None,
                    'direct_object_object_id': direct_object and direct_object.pk or None,
                    'indirect_object_content_type_id': indirect_object and ContentType.objects.get_for_model(indirect_object).id or None,
                    'indirect_object_object_id': indirect_object and indirect_object.pk or None,
                    #'timestamp': timestamp,
                    'context': context,
                    }
                )
        except:
            pass
