import os

import dj_database_url

from johar.settings.base import *  # NOQA

DEBUG = False
ALLOWED_HOSTS = []

DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])

CORS_ALLOWED_ORIGINS = []
