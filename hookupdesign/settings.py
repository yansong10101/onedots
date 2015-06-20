"""
Django settings for hookupdesign project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lz@7$^!s2(%@yx+)2kv-&f!t$qs1p=g0bp(+l7()g2tm2i4u5t'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

INTERNAL_IPS = ("127.0.0.1", )
ALLOWED_HOSTS = ["fierce-savannah-6613.herokuapp.com", ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'twitter_bootstrap',
    'designweb',
    'rest_framework',
    'django_crontab',
    'storages',
)

# 12-30-2014 add for admin utility
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hookupdesign.urls'

WSGI_APPLICATION = 'hookupdesign.wsgi.application'

if os.path.exists("/Users/zys"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),              # enable this while first time setup for local
            'NAME': os.path.join('/Users/zys/workspace', 'db.sqlite3'),  # hard code path for db outside project
        },
    }
else:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get('DATABASE_URL', None))
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# AWS S3 setup
USE_S3 = True
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = 'popdesign'
AWS_QUERYSTRING_AUTH = False
S3_STORAGE = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
S3_URL = 'http://127.0.0.1:8000'   # initial with local for testing
BUCKET_PATH = 'static/products/'
TAX_FILE_PATH = 'static/tax_file/'
IS_TEST = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if USE_S3:
    S3_URL = S3_STORAGE
    if IS_TEST:
        S3_URL = S3_STORAGE + '/test'
        BUCKET_PATH = 'test/static/products/'
    MEDIA_URL = S3_URL + '/products/'
    MEDIA_ROOT = S3_URL

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    MEDIA_ROOT,
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'designweb/../templates'),
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    # 'PAGINATE_BY': 15,
}

EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('SUPPORT_EMAIL', None)
EMAIL_HOST_PASSWORD = os.environ.get('SUPPORT_EMAIL_PASSWORD', None)
EMAIL_USE_TLS = True

CRONJOBS = [
    ('*/1 * * * *', 'designweb.management.commands.group_mail_schedule.testing_call', '> /tmp/last_scheduled_job.log'),
]

# Paypal api section
PAYMENT_SANDBOX = {
    'mode': 'sandbox',  # sandbox or live
    'client_id': os.environ.get('PAYPAL_SANDBOX_CLIENT_ID', None),
    'client_secret': os.environ.get('PAYPAL_SANDBOX_CLIENT_SECRET', None),
}

# MemCache setup
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS',
                                                'mc5.dev.ec2.memcachier.com:11211').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '4cdff9')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '696829c4d1')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'BINARY': True,
        'OPTIONS': {
            'no_block': True,
            'tcp_nodelay': True,
            'tcp_keepalive': True,
            'remove_failed': 4,
            'retry_timeout': 2,
            'dead_timeout': 10,
            '_poll_timeout': 2000
        }
    }
}
