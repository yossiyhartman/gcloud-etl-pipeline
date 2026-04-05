import logging
import os
from datetime import date, timedelta

import polars as pl
from dotenv import load_dotenv
from google.cloud import storage
from pandas.core.algorithms import mode

logger = logging.getLogger(__name__)

load_dotenv()

LANDING_BUCKET_NAME = os.environ["LANDING_BUCKET_NAME"]
RAW_BUCKET_NAME = os.environ["RAW_BUCKET_NAME"]


def ingest_in_raw():
    """TODO: rewrite this function"""

    logger.info("Reading data...")
    df = pl.read_ndjson(source=f"gs://{LANDING_BUCKET_NAME}/*")
    logger.info("Successfuly read data.")

    logger.info("Write to delta..")
    df.write_delta(target=f"gs://{RAW_BUCKET_NAME}", mode="overwrite")
    logger.info("Success ✅")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ingest_in_raw()
