from contextlib import AbstractContextManager, contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session


class PymongoDatabase:
    def __init__(self, db_url: str, echo: bool = True) -> None:

    @contextmanager
    def get_mongodb():
        try:
            with self.() as client:
                db = client["clean-database"]
                yield db
        except Exception as e:
            print(f'Error: {e}')
            raise
