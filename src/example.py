"""
Quick demo: runs through the main GCS operations.
Set BUCKET_NAME and (optionally) GOOGLE_APPLICATION_CREDENTIALS before running.
"""

import os
from storage import (
    get_client,
    get_bucket,
    upload_string,
    download_as_string,
    list_blobs,
    delete_blob,
    generate_signed_url,
)

BUCKET_NAME = os.environ["BUCKET_NAME"]  # e.g. "my-project-bucket"


def main():
    client = get_client()
    bucket = get_bucket(client, BUCKET_NAME)

    # 1. Upload a string as a text file
    upload_string(bucket, "Hello from GCP Starter! 🚀", "hello/world.txt")

    # 2. List objects
    print("\nObjects in bucket:")
    list_blobs(bucket, prefix="hello/")

    # 3. Read it back
    content = download_as_string(bucket, "hello/world.txt")
    print(f"\nContent: {content}")

    # 4. Generate a signed URL
    url = generate_signed_url(bucket, "hello/world.txt", expiration_minutes=30)
    print(f"\nShare this URL:\n{url}")

    # 5. Clean up
    delete_blob(bucket, "hello/world.txt")
    print("\nDone.")


if __name__ == "__main__":
    main()
