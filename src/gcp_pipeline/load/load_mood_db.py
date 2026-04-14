import logging
import os

from dotenv import load_dotenv
from google.cloud.sql.connector import Connector

from gcp_pipeline.connectors.database_connector import DBConnector
from gcp_pipeline.connectors.table_connector import DeltaStorageConnector

logger = logging.getLogger(__name__)

load_dotenv()


def load():
    # config
    RAW_BUCKET_NAME = os.environ["RAW_BUCKET_NAME"]
    DATA_PATH_PREFIX = os.environ["MOOD_FOLDER"]
    INSTANCE_NAME = os.environ["INSTANCE_NAME"]
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_TABLE = os.environ["DB_MOOD_TABLE"]

    delta_connector = DeltaStorageConnector()

    logger.info("Loading data..")

    df = delta_connector.read(f"gs://{RAW_BUCKET_NAME}/{DATA_PATH_PREFIX}")
    logger.info("Loaded. number of rows: %d", len(df))

    with Connector(refresh_strategy="LAZY") as connector:
        logger.info("Connecting to Cloud SQL...")
        db_connector = DBConnector(
            instance_name=INSTANCE_NAME,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        engine = db_connector.create_engine(connector)

        logger.info("Writing to database...")
        df.to_pandas().to_sql(DB_TABLE, engine, index=False, if_exists="replace")
        logger.info("Success! ✅")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    load()
