import polars as pl
from google.cloud.storage import Blob, Bucket
from polars import DataFrame


def get_schema(path: str): ...


def get_latest_files_status(bucket_name: str, path: str) -> DataFrame | None:
    """Retrieve a log file that contains the latest status of the files in the bucket"""
    try:
        return pl.read_delta(f"gs://{bucket_name}/{path}")
    except Exception:
        return None


def get_current_files_status(bucket: Bucket, folder: str) -> list[Blob]:
    """Fetches the metadata (name, last modified time) from the bucket"""
    return list(bucket.list_blobs(prefix=folder, fields="items(name,updated),nextPageToken"))


def get_data_log(path: str): ...
