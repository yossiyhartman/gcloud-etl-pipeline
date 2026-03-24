import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes


class DBConnector:
    def __init__(self, instance_name: str, user: str, password: str, db: str) -> None:
        self.instance_name = instance_name
        self.user = user
        self.password = password
        self.db = db

    def create_engine(self, connector: Connector) -> sqlalchemy.engine.Engine:
        def get_conn():
            return connector.connect(
                self.instance_name,
                "pg8000",
                user=self.user,
                password=self.password,
                db=self.db,
                ip_type=IPTypes.PUBLIC,
            )

        return sqlalchemy.create_engine("postgresql+pg8000://", creator=get_conn)
