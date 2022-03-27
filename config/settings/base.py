"""
Base settings to build other settings files upon.
"""
import datetime
import logging
import os
import sys
from pathlib import Path
import redis
import environ

#
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# # vsphere_monitor/
# APPS_DIR = BASE_DIR / "web"
# env = environ.Env()

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# PROJECT_DIR = BASE_DIR.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'zh-hans'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
    'rest_framework',
    'rest_framework.authtoken',
]
THIRD_PARTY_APPS = [
    "django_celery_beat",
]

LOCAL_APPS = [
    # "vsphere_monitor.users.apps.UsersConfig",
    # Your stuff: custom apps go here
    'apps.authentication.apps.AuthenticationConfig',
    "apps.app.apps.MyAppConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "vsphere_monitor.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "allauth.account.auth_backends.AuthenticationBackend",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'app.UserProfile'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_DIR,  # add statics path
)
STATIC_ROOT = os.path.join(BASE_DIR, "data", "static")

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(BASE_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # "vsphere_monitor.utils.context_processors.settings_context",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(BASE_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN/
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Daniel Roy Greenfeld""", "daniel-roy-greenfeld@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '[%(levelname)s] %(asctime)s | %(name)s:%(lineno)d | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Default logs to stderr
            'formatter': 'normal',  # use the above "normal" formatter
            'level': 'INFO',  # logging level
        },
        'django.server': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
        },
        'debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            # 'backupCount': 10,
            'level': 'DEBUG',
        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'logs', 'info.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            # 'backupCount': 10,
            'level': 'INFO',
        },
        'error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'logs', 'error.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            # 'backupCount': 10,
            'level': 'ERROR',
        },
        'res': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'logs', 'response.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            # 'backupCount': 10,
            'level': 'INFO',
        },

    },
    'loggers': {
        '': {  # means "root logger"
            'handlers': ['error', 'debug', 'console'],  # use the above "console" handler
            'level': 'DEBUG',  # logging level
        },
        'django.server': {
            'handlers': ['console', 'debug'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
        'middleware.log': {
            'handlers': ['console', 'res'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# Your stuff...
# ------------------------------------------------------------------------------


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 必須有

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.backends.api.TokenAuthentication',  # <-- And here
        'authentication.backends.api.AccessKeyAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

EXPIRING_TOKEN_LIFESPAN = datetime.timedelta(days=1)
# EXPIRING_TOKEN_LIFESPAN = datetime.timedelta(minutes=3)


# IMGUR
# ------------------------------------------------------------------------------
IMAGE_DIR = BASE_DIR / 'static' / 'files' / 'image'
IMGUR_ID = env.str('IMGUR_ID', '')
IMGUR_SECRET = env.str('IMGUR_SECRET', '')

# TELEGRAM_BOT_TOKEN

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = env.str('TELEGRAM_CHANNEL_ID', '')

BOOTSTRAP_TOKEN = env.str('BOOTSTRAP_TOKEN', '')

# ---- Redis ----

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")
redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,decode_responses=True)

# ---- CELERY v4.4.6 -----

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
# export CELERY_BROKER_URL="${REDIS_URL}"
# CELERY_BROKER_URL = os.environ.get("REDIS_URL")
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
CELERY_BROKER_URL = 'amqp://admin:112e76122ffaec98209aacf6@localhost:5672//rss'
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'rpc://'

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# CELERY_TASK_TIME_LIMIT = 10 * 60
CELERYD_TIME_LIMIT = 10 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# CELERY_TASK_SOFT_TIME_LIMIT = 300
CELERYD_SOFT_TIME_LIMIT = 300
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# 防治死锁
# CELERYD_FORCE_EXECV = True

# celery 的启动工作数量设置
# CELERY_WORKER_CONCURRENCY = 20

# 任务预取功能，就是每个工作的进程／线程在获取任务的时候，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
# CELERYD_PREFETCH_MULTIPLIER = 20

# CELERY_ACKS_LATE=''

# 每個worker執行了多少任務就會銷燬，防止記憶體洩露，預設是無限的
# CELERYD_MAX_TASKS_PER_CHILD = 40

# 是否存儲任務返回值（邏輯刪除）。如果您仍然想存儲錯誤，只是不成功返回值，則可以設置
# CELERY_IGNORE_RESULT = True

# 任务结果的时效时间，默认一天
# CELERY_TASK_RESULT_EXPIRES = 0
# CELERY_RESULT_EXPIRES = 0
