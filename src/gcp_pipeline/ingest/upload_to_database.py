import logging
import os

from dotenv import load_dotenv
from google.cloud.sql.connector import Connector

from gcp_pipeline.connect.database_connector import DBConnector
from gcp_pipeline.extract.read_from_bucket import load_all

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_PATH = "gs://" + os.getenv("BUCKET_NAME", "")
PROJECT_NAME = os.getenv("PROJECT_NAME", "")
REGION = os.getenv("REGION", "")
DB_INSTANCE_NAME = os.getenv("DB_INSTANCE_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "")


def ingest_in_database():

    logger.info("Loading data..")
    df = load_all(BUCKET_PATH)
    logger.info("Loaded. number of rows: %d", len(df))

    with Connector(refresh_strategy="LAZY") as connector:
        logger.info("Connecting to Cloud SQL...")
        db_connector = DBConnector(
            instance_name=f"{PROJECT_NAME}:{REGION}:{DB_INSTANCE_NAME}",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        engine = db_connector.create_engine(connector)

        try:
            logger.info("Writing to database...")

            df.to_sql("mood", engine, index=False, if_exists="replace")

            logger.info("Success! ✅")

        except Exception as e:
            logger.exception("Connection failed", exc_info=e)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    ingest_in_database()
