from pymongo import MongoClient


class PymongoBaseRepository:
    def __init__(self, db_url: str, client: MongoClient):
        self._client = client
        self.database = self._client[db_url]

    @property
    def mongo_client(self) -> MongoClient:
        return self._client
