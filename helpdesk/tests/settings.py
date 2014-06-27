import os, sys
PROJECT_DIR = os.path.dirname(__file__)
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        # Don't do this. It dramatically slows down the test.
#        'NAME': '/tmp/helpdesk.db',
#        'TEST_NAME': '/tmp/helpdesk.db',
    }
}
ROOT_URLCONF = 'helpdesk.tests.urls'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    
    'helpdesk',
    'helpdesk.tests',
]
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
SOUTH_TESTS_MIGRATE = False
USE_TZ = True

AUTH_USER_MODEL = 'auth.User'

SECRET_KEY = 'secret'

SITE_ID = 1

BASE_SECURE_URL = 'https://localhost'
BASE_URL = 'http://localhost'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

STATIC_URL = '/static/'
