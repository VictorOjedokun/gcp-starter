"""Unit tests — GCS calls are mocked so no real credentials are needed."""

from unittest.mock import MagicMock, patch
import pytest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from storage import upload_string, download_as_string, list_blobs, delete_blob


@pytest.fixture
def mock_bucket():
    bucket = MagicMock()
    bucket.name = "test-bucket"
    return bucket


def test_upload_string(mock_bucket):
    uri = upload_string(mock_bucket, "hello", "test/hello.txt")
    mock_bucket.blob.assert_called_once_with("test/hello.txt")
    mock_bucket.blob().upload_from_string.assert_called_once_with("hello", content_type="text/plain")
    assert uri == "gs://test-bucket/test/hello.txt"


def test_download_as_string(mock_bucket):
    mock_bucket.blob().download_as_text.return_value = "hello"
    content = download_as_string(mock_bucket, "test/hello.txt")
    assert content == "hello"


def test_list_blobs(mock_bucket):
    blob1, blob2 = MagicMock(name="a.txt"), MagicMock(name="b.txt")
    blob1.name, blob2.name = "a.txt", "b.txt"
    mock_bucket.list_blobs.return_value = [blob1, blob2]
    names = list_blobs(mock_bucket)
    assert names == ["a.txt", "b.txt"]


def test_delete_blob(mock_bucket):
    delete_blob(mock_bucket, "test/hello.txt")
    mock_bucket.blob().delete.assert_called_once()
