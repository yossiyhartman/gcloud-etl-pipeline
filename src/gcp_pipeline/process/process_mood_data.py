import json
import logging
import os
from io import StringIO

import polars as pl
from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.storage import Bucket

from gcp_pipeline.file_status_log import FileStatusLog
from gcp_pipeline.schema_validator import SchemaValidator

load_dotenv()

LANDING_BUCKET_NAME = os.getenv("LANDING_BUCKET_NAME", "")
META_BUCKET_NAME = os.getenv("META_BUCKET_NAME", "")
RAW_BUCKET_NAME = os.getenv("RAW_BUCKET_NAME", "")
SCHEMA_BUCKET_NAME = os.getenv("SCHEMA_BUCKET_NAME", "")

MOOD_PREFIX = "mood"
MOOD_SCHEMA_FILE = "mood_schema.json"

logger = logging.getLogger(__name__)


def get_current_files_status(bucket: Bucket, prefix: str) -> pl.DataFrame:
    """Fetch file metadata (name, updated timestamp) from GCS."""

    blobs = bucket.list_blobs(prefix=prefix, fields="items(name,updated),nextPageToken")
    data = [{"name": blob.name, "updated": blob.updated} for blob in blobs]

    schema = {"name": pl.String, "updated": pl.Datetime(time_zone="UTC")}

    if not data:
        return pl.DataFrame(schema=schema)

    return pl.DataFrame(data, schema=schema)


def load_schema(bucket: Bucket, schema_path: str) -> dict:
    """Load JSON schema from GCS."""
    blob = bucket.get_blob(schema_path)
    if blob is None:
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    return json.loads(blob.download_as_bytes())


def validate_ndjson(data: str, validator: SchemaValidator) -> bool:
    """Validate NDJSON string against schema."""
    for line in data.splitlines():
        if not line.strip():
            continue

        record = json.loads(line)

        if not validator.is_valid(record):
            return False

    return True


def process_files(bucket: Bucket, files: list[str], validator: SchemaValidator) -> list[pl.DataFrame]:
    """Download, validate, and parse files into DataFrames."""
    valid_dataframes: list[pl.DataFrame] = []

    for file in files:
        logger.info(f"Processing file: {file}")

        blob = bucket.get_blob(file)
        if blob is None:
            logger.warning(f"File not found: {file}")
            continue

        data = blob.download_as_text()

        if validate_ndjson(data, validator):
            df = pl.read_ndjson(StringIO(data))
            valid_dataframes.append(df)
        else:
            logger.warning(f"Validation failed for file: {file}")

    return valid_dataframes


def process_mood_data() -> None:
    """Main pipeline for processing mood data."""

    client = storage.Client()
    landing_bucket = client.bucket(LANDING_BUCKET_NAME)
    schema_bucket = client.bucket(SCHEMA_BUCKET_NAME)

    file_status_log = FileStatusLog(META_BUCKET_NAME, MOOD_PREFIX)

    latest_status = file_status_log.get_latest_file_status()
    current_status = get_current_files_status(landing_bucket, MOOD_PREFIX)

    files_to_update = file_status_log.get_files_to_update(latest_status=latest_status, cur_status=current_status)

    logger.info("Detected %d files to update.", len(files_to_update))

    if not files_to_update:
        return

    schema = load_schema(schema_bucket, MOOD_SCHEMA_FILE)
    validator = SchemaValidator(schema)

    dataframes = process_files(landing_bucket, files_to_update, validator)

    if not dataframes:
        logger.warning("No valid data to write.")
        return

    df = pl.concat(dataframes, how="vertical")

    output_path = f"gs://{RAW_BUCKET_NAME}/{MOOD_PREFIX}"
    df.write_delta(output_path, mode="overwrite")

    logger.info(f"Data written to {output_path}")

    file_status_log.update_log(cur_status=current_status)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    process_mood_data()
