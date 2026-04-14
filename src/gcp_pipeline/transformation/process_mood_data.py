import json
import logging
import os

import polars as pl
from dotenv import load_dotenv
from google.cloud.storage import Blob

from gcp_pipeline.connectors import GCPConnector
from gcp_pipeline.serialization import NDJSONSerializer
from gcp_pipeline.utils import get_current_files_status
from gcp_pipeline.validation import JSONSchemaValidator

load_dotenv()

logger = logging.getLogger(__name__)


def transform_data():
    """Main pipeline for processing data."""

    # config
    LANDING_BUCKET_NAME = os.environ["LANDING_BUCKET_NAME"]
    META_BUCKET_NAME = os.environ["META_BUCKET_NAME"]
    RAW_BUCKET_NAME = os.environ["RAW_BUCKET_NAME"]
    SCHEMA_BUCKET_NAME = os.environ["SCHEMA_BUCKET_NAME"]
    SCHEMA_FILE = os.environ["MOOD_SCHEMA_FILE"]
    DATA_PATH_PREFIX = os.environ["MOOD_FOLDER"]

    serializer = NDJSONSerializer()
    landing_bucket = GCPConnector(bucket=LANDING_BUCKET_NAME)
    schema_bucket = GCPConnector(bucket=SCHEMA_BUCKET_NAME)

    logger.info("Get the current status of the files in: %s", DATA_PATH_PREFIX)
    current_status = get_current_files_status(landing_bucket.bucket, DATA_PATH_PREFIX)

    try:
        logger.info("Get the latest status of the files in: %s", DATA_PATH_PREFIX)
        latest_status = pl.read_delta(f"gs://{META_BUCKET_NAME}/{DATA_PATH_PREFIX}")
    except Exception:
        # If no status log is found, assume no earlier status is logged. Start with clean Dataframe.
        logger.warning("No status found. Assume no earlier status is logged.")
        latest_status = pl.DataFrame(schema={"name": pl.String, "updated": pl.Datetime(time_zone="UTC")})

    logger.info("Compare statuses and return differences")
    joined_statuses = current_status.join(latest_status, on="name", how="left", suffix="_latest")
    changed_statuses = joined_statuses.filter(pl.col("updated").ne_missing(pl.col("updated_latest")))
    changed_file_names = changed_statuses["name"].to_list()

    if not changed_file_names:
        logger.info("Nothing has to be updated.")
        return

    logger.info("Found %d updated files", len(changed_file_names))

    schema: Blob = schema_bucket.read(f"{SCHEMA_FILE}")
    validator = JSONSchemaValidator(json.loads(schema.download_as_bytes()))

    df_changed_files: list[pl.DataFrame] = []

    for file in changed_file_names:
        logger.info(f"Processing file: {file}")

        blob = landing_bucket.read(file)
        data = blob.download_as_text()
        records = serializer.read(data)

        for record in records:
            if not validator.is_valid(record):
                logger.warning(f"Validation failed for file: {file}")
                break
        else:
            df_changed_files.append(pl.DataFrame(records))

    if not df_changed_files:
        logger.warning("No valid data to write.")
        return

    df = pl.concat(df_changed_files, how="vertical")

    output_path = f"gs://{RAW_BUCKET_NAME}/{DATA_PATH_PREFIX}"
    logger.info(f"Write new data to {output_path}")
    df.write_delta(f"gs://{RAW_BUCKET_NAME}/{DATA_PATH_PREFIX}", mode="overwrite")
    logger.info("Success")

    output_path = f"gs://{META_BUCKET_NAME}/{DATA_PATH_PREFIX}"
    logger.info(f"Update status log: {output_path}")
    current_status.write_delta(f"gs://{META_BUCKET_NAME}/{DATA_PATH_PREFIX}", mode="overwrite")
    logger.info("Success")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    transform_data()
