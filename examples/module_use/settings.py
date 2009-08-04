import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG


SITE_ROOT = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..'))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'database.tmp~')

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'activitystreams',
    'piston',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_DIRS = (
    '%s/templates' % SITE_ROOT,
)
