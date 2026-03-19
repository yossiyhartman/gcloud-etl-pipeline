import logging
import os

import pyarrow as pa
import pyarrow.dataset as ds
from dotenv import load_dotenv

from gcp_pipeline.generate.data_generator import DataGenerator

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_PATH = "gs://" + os.getenv("BUCKET_NAME", "")


def ingest_in_storage():

    logger.info("Generating data...")
    data = DataGenerator().generate(n_records=1)

    # Convert to Arrow table
    table = pa.table(data)

    logger.info("Writing dataset to bucket...")

    ds.write_dataset(
        table,
        base_dir=BUCKET_PATH,
        format="parquet",
        partitioning=["event_time"],
        existing_data_behavior="overwrite_or_ignore",
    )

    logger.info("Success! ✅")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    ingest_in_storage()
