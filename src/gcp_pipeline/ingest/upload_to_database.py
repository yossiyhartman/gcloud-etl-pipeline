import logging
import os

import sqlalchemy
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes

load_dotenv()

logger = logging.getLogger(__name__)


def create_engine(connector: Connector) -> sqlalchemy.engine.Engine:

    instance_connection_name = os.environ["CONNECTION_NAME"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    return sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        ),
    )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("Connecting to Cloud SQL...")

    with Connector(refresh_strategy="LAZY") as connector:
        engine = create_engine(connector)

        try:
            with engine.connect() as conn:
                logger.info("Running test query...")
                result = conn.execute(sqlalchemy.text("SELECT 1"))
                logger.info(f"Success: {result.scalar()}")

        except Exception:
            logger.exception("Connection failed")


if __name__ == "__main__":
    main()
