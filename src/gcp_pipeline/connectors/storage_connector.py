from typing import Any, Protocol

from google.cloud import storage
from google.cloud.storage import Blob, Bucket, Client


class ObjectStorageConnector(Protocol):
    """"""

    def write(self, path: str, data: Any) -> None:
        """"""
        ...

    def read(self, path: str) -> Any:
        """"""
        ...


class GCPConnector:
    def __init__(self, bucket: str) -> None:
        self.client: Client = storage.Client()
        self.bucket: Bucket = self.client.bucket(bucket)

    def read(self, path: str) -> Blob:
        """"""
        blob = self.bucket.get_blob(path)

        if blob is None:
            raise FileNotFoundError("Could not find blob")

        return blob

    def write(self, path: str, data: Any) -> None:
        """"""
        self.bucket.blob(path).upload_from_string(data)
