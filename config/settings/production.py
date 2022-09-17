from .base import *  # noqa

import io
import os
import google.auth
from google.cloud import secretmanager
from google.oauth2 import service_account

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")



# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("MYSQL_DATABASE"),
        'HOST': os.environ.get("MYSQL_HOST"),
        'PORT': os.environ.get("MYSQL_PORT"),
        'USER': os.environ.get("MYSQL_USER"),
        'PASSWORD': os.environ.get("MYSQL_ROOT_PASSWORD"),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}



GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    BASE_DIR / 'credentials.json'
)

DEFAULT_FILE_STORAGE = 'src.gcloud.GoogleCloudMediaFileStorage'
STATICFILES_STORAGE = 'src.gcloud.GoogleCloudStaticFileStorage'
GS_MEDIA_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME")
GS_STATIC_BUCKET_NAME = env("GS_STATIC_BUCKET_NAME")
GS_PROJECT_ID = env("GS_PROJECT_ID")
MEDIA_URL = f'https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/'
# GS_DEFAULT_ACL = 'publicRead'
# GS_QUERYSTRING_AUTH = False
# GS_DEFAULT_ACL = None

