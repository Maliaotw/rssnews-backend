from .base import *  # noqa

import io
import os
import google.auth
from google.cloud import secretmanager
from google.oauth2 import service_account


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

