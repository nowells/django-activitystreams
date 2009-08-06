import logging

from django.conf import settings
from activitystreams.clients import ActivityStream

logger = logging.getLogger(__name__)

class SiteActivityMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and not (request.path_info.startswith('/media/') or '/api/' in request.path_info):
            activity_stream = ActivityStream()
            activity_stream.record_activity(
                'site_page_view',
                request.user.username,
                request.user,
                request.user,
                extra={
                    'username': request.user.username,
                    'request_path': request.get_full_path()
                    }
                )
