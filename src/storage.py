"""
GCP Cloud Storage helper module.
Covers: upload, download, list, delete, and signed URL generation.
"""

import os
from pathlib import Path
from datetime import timedelta

from google.cloud import storage
from google.oauth2 import service_account


def get_client(credentials_path: str | None = None) -> storage.Client:
    """
    Return a GCS client.
    - If GOOGLE_APPLICATION_CREDENTIALS env var is set, it's picked up automatically.
    - Pass credentials_path explicitly to override.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return storage.Client(credentials=credentials)
    return storage.Client()


# ── Bucket helpers ────────────────────────────────────────────────────────────

def create_bucket(client: storage.Client, bucket_name: str, location: str = "US") -> storage.Bucket:
    bucket = client.create_bucket(bucket_name, location=location)
    print(f"Bucket {bucket.name} created in {location}.")
    return bucket


def get_bucket(client: storage.Client, bucket_name: str) -> storage.Bucket:
    return client.bucket(bucket_name)


# ── Object helpers ────────────────────────────────────────────────────────────

def upload_file(
    bucket: storage.Bucket,
    source_path: str,
    destination_blob: str | None = None,
) -> str:
    """Upload a local file; returns the GCS URI."""
    destination_blob = destination_blob or Path(source_path).name
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_path)
    uri = f"gs://{bucket.name}/{destination_blob}"
    print(f"Uploaded {source_path} → {uri}")
    return uri


def upload_string(
    bucket: storage.Bucket,
    content: str,
    destination_blob: str,
    content_type: str = "text/plain",
) -> str:
    """Upload a string directly (no local file needed)."""
    blob = bucket.blob(destination_blob)
    blob.upload_from_string(content, content_type=content_type)
    uri = f"gs://{bucket.name}/{destination_blob}"
    print(f"Uploaded string → {uri}")
    return uri


def download_file(
    bucket: storage.Bucket,
    source_blob: str,
    destination_path: str,
) -> None:
    """Download a GCS object to a local file."""
    blob = bucket.blob(source_blob)
    blob.download_to_filename(destination_path)
    print(f"Downloaded gs://{bucket.name}/{source_blob} → {destination_path}")


def download_as_string(bucket: storage.Bucket, source_blob: str) -> str:
    """Download a GCS object and return its content as a string."""
    blob = bucket.blob(source_blob)
    return blob.download_as_text()


def list_blobs(bucket: storage.Bucket, prefix: str = "") -> list[str]:
    """List object names in a bucket, optionally filtered by prefix."""
    blobs = bucket.list_blobs(prefix=prefix)
    names = [b.name for b in blobs]
    for name in names:
        print(f"  {name}")
    return names


def delete_blob(bucket: storage.Bucket, blob_name: str) -> None:
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"Deleted gs://{bucket.name}/{blob_name}")


def generate_signed_url(
    bucket: storage.Bucket,
    blob_name: str,
    expiration_minutes: int = 15,
) -> str:
    """
    Generate a V4 signed URL (temporary public link).
    Requires a service account key — ADC / metadata server won't work here.
    """
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )
    print(f"Signed URL (expires in {expiration_minutes}m): {url}")
    return url
