"""
1 - Importing settings file to access locations.
2 - Importing S3 storage class to access S3 on collect static.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Setting static files storages to location
    specified in settings.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Setting media files storages to location
    specified in settings.
    """
    location = settings.MEDIAFILES_LOCATION
