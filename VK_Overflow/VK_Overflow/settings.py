from os import getenv
from pathlib import Path

from django.conf import settings
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env')

SECRET_KEY = getenv('DJANGO_SECRET_KEY')

DEBUG = getenv('DJANGO_DEBUG', '0').lower() in ('1', 'true', 't', 'y', 'yes')
ALLOWED_HOSTS = list(getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(','))
INTERNAL_IPS = list(getenv('DJANGO_INTERNAL_IPS', '127.0.0.1,localhost').split(','))

MEMCACHED_HOST = getenv("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = getenv("MEMCACHED_PORT", "11211")


if DEBUG:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'core.apps.CoreConfig',
    'questions.apps.QuestionsConfig',
    'users.apps.UsersConfig',

    # 3rd-party apps
    'sorl.thumbnail',
]
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if settings.DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


ROOT_URLCONF = 'VK_Overflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'questions.context_processors.get_popular_tags',
                'questions.context_processors.get_most_active_users',
            ],
        },
    },
]

WSGI_APPLICATION = 'VK_Overflow.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB', 'VK_Overflow'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': getenv('POSTGRES_HOST', 'localhost'),
        'PORT': getenv('POSTGRES_PORT', '5432'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': f'{MEMCACHED_HOST}:{MEMCACHED_PORT}',  # noqa: E231
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'

# Uncomment if you will use S3-like storage (https://github.com/jazzband/sorl-thumbnail/issues/351)
# THUMBNAIL_FORCE_OVERWRITE = True
