import os

import sqlalchemy
from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud.sql.connector import Connector

from gcp_pipeline.connect.database_connector import DBConnector

load_dotenv()

app = FastAPI()

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "")

connector = Connector(refresh_strategy="LAZY")

db_connector = DBConnector(
    instance_name=INSTANCE_NAME,
    user=DB_USER,
    password=DB_PASS,
    db=DB_NAME,
)
engine = db_connector.create_engine(connector)


@app.get("/")
def hello():
    return "Hello visitor"


@app.get("/data")
def read_data():

    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM mood"))
        rows = [dict(row._mapping) for row in result]
    return {"data": rows}
