DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'database.tmp~')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'activitystreams',
)

ROOT_URLCONF = 'urls'
