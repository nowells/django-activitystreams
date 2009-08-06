from activitystreams import settings
from django.contrib.contenttypes.models import ContentType
from wellrested import JsonRestClient

class ActivityStream(object):
    def __init__(self):
        self._client = JsonRestClient(settings.ACTIVITYSTREAMS_BASE_URL, settings.ACTIVITYSTREAMS_USERNAME, settings.ACTIVITYSTREAMS_PASSWORD)

    def record_activity(self, action_slug=None, user_id=None, direct_object=None, indirect_object=None, timestamp=None, extra=None):
        try:
            response = self._client.post(
                '%s/activities.json' % settings.ACTIVITYSTREAMS_SOURCE,
                data={
                    'user_id': user_id,
                    'action_slug': action_slug,
                    'direct_object_content_type_id': direct_object and ContentType.objects.get_for_model(direct_object).id or None,
                    'direct_object_object_id': direct_object and direct_object.pk or None,
                    'indirect_object_content_type_id': indirect_object and ContentType.objects.get_for_model(indirect_object).id or None,
                    'indirect_object_object_id': indirect_object and indirect_object.pk or None,
                    'timestamp': timestamp,
                    'extra_data': extra,
                    }
                )
            raise Exception()
        except:
            raise
