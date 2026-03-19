import logging
import os

import sqlalchemy
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes

from gcp_pipeline.extract.read_from_bucket import load_all

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_PATH: str = os.environ.get("BUCKET_PATH", "")

INSTANCE_CONNECTION_NAME = os.environ.get("CONNECTION_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "")

TABLE_NAME = os.environ.get("TABLE_NAME", "")


def create_engine(connector: Connector) -> sqlalchemy.engine.Engine:

    def get_conn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type=IPTypes.PUBLIC,
        )

    return sqlalchemy.create_engine("postgresql+pg8000://", creator=get_conn)


def ingest_in_database():
    logger.info("Loading data..")
    df = load_all(BUCKET_PATH)
    logger.info("Loaded. number of rows: %d", len(df))

    with Connector(refresh_strategy="LAZY") as connector:
        logger.info("Connecting to Cloud SQL...")
        engine = create_engine(connector)

        try:
            logger.info("Writing to database...")

            df.to_sql(TABLE_NAME, engine, if_exists="replace")

            logger.info("Success! ✅")

        except Exception as e:
            logger.exception("Connection failed", exc_info=e)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    ingest_in_database()
