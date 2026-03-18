import logging
import os

import pyarrow as pa
import pyarrow.dataset as ds

from gcp_pipeline.generate.data_generator import DataGenerator

BUCKET_PATH = os.getenv("BUCKET_PATH")

logger = logging.getLogger()


def main():

    # Generate some dummy data
    logger.info("generating data...")
    data = DataGenerator().generate(n_records=1)

    logger.info(data)

    # Create a pyarrow table
    table = pa.table(data)

    logger.info("Writing to bucket...")
    # Upload the data to gcp, and partition on the event-time
    ds.write_dataset(
        table,
        base_dir=BUCKET_PATH,
        format="parquet",
        partitioning=["event_time"],
        existing_data_behavior="overwrite_or_ignore",
    )
    logger.info("Success!")


if __name__ == "__main__":
    logging.basicConfig(level=0)
    main()
