import logging
import os

import polars as pl
from dotenv import load_dotenv
from google.cloud import storage

from gcp_pipeline.utils import get_current_files_status, get_latest_files_status

logger = logging.getLogger(__name__)

load_dotenv()

LANDING_BUCKET_NAME = os.environ["LANDING_BUCKET_NAME"]
RAW_BUCKET_NAME = os.environ["RAW_BUCKET_NAME"]
META_BUCKET_NAME = os.environ["META_BUCKET_NAME"]
SCHEMA_BUCKET_NAME = os.environ["SCHEMA_BUCKET_NAME"]


def process_mood_data():
    """TODO: rewrite this function"""
    # Get client
    client = storage.Client()
    landing_bucket = client.bucket(LANDING_BUCKET_NAME)

    # -- Check which files to update
    # 01: Get the latest meta data on the log update file. Now you know which data needs to be pulled in.
    # df_latest_status_files = get_latest_files_status(LANDING_BUCKET_NAME, "mood")

    # 02: Using the google client library, pull in the files and their metadata
    blobs_current_status_files = get_current_files_status(landing_bucket, folder="mood")

    df_current_status_files = pl.DataFrame(
        [{"name": blob.name, "updated": blob.updated} for blob in blobs_current_status_files]
    )
    df_current_status_files.show()
    # 03: Compare current with latest. Collect all files that need to be pulled in
    ...
    # 04: Do not update meta data yet. Park it till later.
    ...

    # -- Validate incomming files
    # 01: get the predifined schema for the mood data
    # 02: for each file, validate the incomming data against the schema
    # 03: if there are discrapancies, apply logic or isolate
    # 04: Log incorrect files
    #
    # -- Convert to Delta
    # 01: Check if delta table exist
    # 02: If not, create with required configuration, else take delta
    # 03: update delta table accordingly.


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    process_mood_data()
