import polars as pl
from google.cloud.storage import Bucket


def get_current_files_status(bucket: Bucket, prefix: str) -> pl.DataFrame:
    """Fetch file metadata (name, updated timestamp) from GCS."""

    blobs = bucket.list_blobs(prefix=prefix, fields="items(name,updated),nextPageToken")
    data = [{"name": blob.name, "updated": blob.updated} for blob in blobs]
    schema = {"name": pl.String, "updated": pl.Datetime(time_zone="UTC")}

    if not data:
        return pl.DataFrame(schema=schema)

    return pl.DataFrame(data, schema=schema)
