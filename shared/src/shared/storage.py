from minio import Minio
from minio.error import S3Error
from datetime import timedelta
import os
import logging
from shared.config import SETTINGS

logger = logging.getLogger(__name__)

client = Minio(
    endpoint=SETTINGS.MINIO_ENDPOINT,
    access_key=SETTINGS.MINIO_ACCESS_KEY,
    secret_key=SETTINGS.MINIO_SECRET_KEY,
    secure=SETTINGS.MINIO_SECURE
)

def ensure_bucket(bucket_name: str):
    """Create the bucket if it doesn’t already exist."""
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except S3Error as err:
        logger.error(f"Failed to ensure bucket {bucket_name}: {err}")
        raise
    
def upload_file(bucket_name: str,
                object_name: str,
                file_path: str,
                content_type: str = None):
    """
    Upload a local file to MinIO.
    Good for testing with existing files on disk.
    """
    ensure_bucket(bucket_name)
    try:
        client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )
        logger.info(f"Uploaded file {file_path} → {bucket_name}/{object_name}")
    except S3Error as err:
        logger.error(f"upload_file failed for {file_path}: {err}")
        raise

def upload_stream(bucket_name: str,
                  object_name: str,
                  stream,
                  length: int,
                  content_type: str = "application/octet-stream",
                  max_retries: int = 3):
    """
    Stream data directly into MinIO, retrying on transient errors.
    
    Args:
      bucket_name: target bucket
      object_name: object key within the bucket
      stream: file-like object (e.g. HTTPResponse.raw)
      length: total size in bytes
      content_type: MIME type
      max_retries: how many times to retry on failure
    """
    ensure_bucket(bucket_name)
    
    for attempt in range(1, max_retries + 1):
        try:
            client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=stream,
                length=length,
                content_type=content_type
            )
            # If we get here, upload succeeded
            logger.info(f"Uploaded {object_name} to {bucket_name}")
            return
        except S3Error as err:
            logger.warning(f"Upload attempt {attempt} failed for {object_name}: {err}")
            if attempt == max_retries:
                logger.error(f"Exceeded retries for uploading {object_name}")
                raise
            # Rewind the stream if possible or re-open it before retrying
            if hasattr(stream, "seek"):
                stream.seek(0)

def get_presigned_url(bucket_name: str,
                      object_name: str,
                      expires: timedelta = timedelta(hours=1)):
    """
    Return a time-limited URL for accessing this object.
    """
    try:
        return client.get_presigned_url(
            "GET",
            bucket_name,
            object_name,
            expires=expires
        )
    except S3Error as err:
        logger.error(f"Failed to generate presigned URL for {object_name}: {err}")
        raise
