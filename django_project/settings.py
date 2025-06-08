import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ — лучше передавать через переменную окружения
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-4ju2n@$f9d0c=h)_g0lbb%k9&@rf(xa$d$g$&5ri$uf)*gev^4')

# Определяем режим debug по переменной окружения
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Разрешенные хосты — можно также передавать через переменную окружения
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,yourdomain.com').split(',')

CSRF_TRUSTED_ORIGINS = [
    "https://*.replit.dev",
    "https://*.replit.app",
    "https://*.id.repl.co",
    f"https://{os.environ.get('REPL_SLUG', '')}.replit.dev",
    f"https://{os.environ.get('REPL_ID', '')}.id.repl.co",
    "https://77cf698a-669f-4596-b46a-67dffadfdf23-00-stesj4g2kuha.sisko.replit.dev",
    "https://77cf698a-669f-4596-b46a-67dffadfdf23-00-stesj4g2kuha.sisko.replit.dev:8000",
    "https://06e830e2-b019-41aa-8f6b-81510d844989-00-j94ijnubinm8.sisko.replit.dev",
    "https://06e830e2-b019-41aa-8f6b-81510d844989-00-j94ijnubinm8.sisko.replit.dev:8000",
    "https://77a983bf-f017-45e3-8c57-0a7d7da9f13b-00-27qdpk93g7fbp.sisko.replit.dev",
    "https://77a983bf-f017-45e3-8c57-0a7d7da9f13b-00-27qdpk93g7fbp.sisko.replit.dev:8000",
]

# Настройки cookie безопасности по умолчанию
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'

# Если мы на Replit — изменяем настройки cookie и debug
if 'REPLIT' in os.environ:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SAMESITE = 'Lax'
    DEBUG = True

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

if "REPLIT_DEPLOYMENT" in os.environ:
    MIDDLEWARE.append('django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'django_project.urls'
ASGI_APPLICATION = 'django_project.asgi.application'

# Используем InMemory для локальной разработки, Redis для продакшена
if DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379')],
            },
        },
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django_db'),
        'USER': os.getenv('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'django_pass'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
