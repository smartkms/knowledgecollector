from minio import Minio
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Read settings
ENDPOINT = os.getenv("MINIO_ENDPOINT")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

# Create client
client = Minio(
    endpoint=ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=SECURE
)


def ensure_bucket(bucket_name: str):
    """Create bucket if it doesn't exist."""
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def upload_bytes(
    bucket: str,
    object_name: str,
    data: bytes,
    content_type: str = "application/octet-stream",
):
    """Upload raw bytes (e.g. file download) to MinIO."""
    ensure_bucket(bucket)
    client.put_object(
        bucket_name=bucket,
        object_name=object_name,
        data=data,
        length=len(data),
        content_type=content_type,
    )


def upload_file(
    bucket: str, object_name: str, file_path: str, content_type: str = None
):
    """Upload a local file to MinIO."""
    ensure_bucket(bucket)
    client.fput_object(bucket, object_name, file_path, content_type=content_type)
