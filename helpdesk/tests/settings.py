import os

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

# Disable migrations.
# http://stackoverflow.com/a/28560805/247542
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"
SOUTH_TESTS_MIGRATE = False # <= Django 1.8
# if django.VERSION > (1, 7, 0): # > Django 1.8 
#     MIGRATION_MODULES = DisableMigrations()

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

MIDDLEWARE = MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                # Defaults:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Our extra:
                "django.template.context_processors.request",
            ),
        },
    },
]
