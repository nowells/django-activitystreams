from django.conf import settings

ACTIVITYSTREAMS_BASE_URL = getattr(settings, 'ACTIVITYSTREAMS_BASE_URL', 'http://localhost:8000/api/activitystreams/')
ACTIVITYSTREAMS_SOURCE = getattr(settings, 'ACTIVITYSTREAMS_SOURCE', 'local')
ACTIVITYSTREAMS_USERNAME = getattr(settings, 'ACTIVITYSTREAMS_USERNAME', 'root')
ACTIVITYSTREAMS_PASSWORD = getattr(settings, 'ACTIVITYSTREAMS_PASSWORD', 'root')
