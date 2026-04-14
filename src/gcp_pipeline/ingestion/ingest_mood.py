import logging
import os

from dotenv import load_dotenv

from gcp_pipeline.connectors.storage_connector import GCPConnector
from gcp_pipeline.serialization import NDJSONSerializer
from gcp_pipeline.simulation import MoodDataSimulator

load_dotenv()

logger = logging.getLogger(__name__)


def ingest():
    BUCKET_NAME = os.environ["LANDING_BUCKET_NAME"]
    FOLDER = os.environ["MOOD_FOLDER"]
    N_DAYS = 2  # Number of days to generate data

    storage = GCPConnector(bucket=BUCKET_NAME)
    serializer = NDJSONSerializer()
    simulator = MoodDataSimulator()

    # Generate
    logger.info("Generating mood data ...")
    data = simulator.generate(n_days=N_DAYS)
    logger.info("Generation complete")

    # Ingest
    logger.info("Ingesting %d records into bucket: %s | folder: %s", len(data), BUCKET_NAME, FOLDER)
    for daily_records in data:
        # A quick method to get the date for the partition
        day = daily_records[0].get("date", "no_date")

        ndjson_data = serializer.write(daily_records)

        storage.write(data=ndjson_data, path=f"{FOLDER}/{day}.ndjson")

    logger.info("Ingestion complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ingest()
