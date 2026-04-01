import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from google.cloud import storage

from gcp_pipeline.generate.mood_data_generator import MoodDataGenerator

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_NAME = os.environ["LANDING_BUCKET_NAME"]


def ingest_in_landing() -> None:

    # Partition also by the request time later
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Generate
    gen_data = MoodDataGenerator().generate(n_days=10)

    # Create a connection
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    for day in gen_data:
        for event_time, records in day.items():
            # Partition Path
            path = f"event_time={event_time}/upload_date={request_time}/data.ndjson"

            # Parse the data such that every dict is on its own line
            ndjson_data = "\n".join(json.dumps(r) for r in records)

            # Set the destination path
            blob = bucket.blob(path)

            logger.info("Writing data to bucket for: %s", event_time)
            blob.upload_from_string(ndjson_data)
            logger.info("Success! ✅")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ingest_in_landing()
