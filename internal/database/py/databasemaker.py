import os
from typing import Any

import psycopg2


class ConfigSQL:
    def __init__(self):
        path = os.getenv("SQL_PATH")
        # path = "/app/database/sql"
        self.CREATE_FILE = f"{path}/create_tables.sql"
        self.DROP_FILE = f"{path}/drop_tables.sql"
        self.COPY_FILE = f"{path}/copy_tables.sql"
        self.CONSTRAINTS_FILE = f"{path}/constraints.sql"


class DatabaseMaker:
    connection: Any
    cursor: Any

    def __init__(self, is_test_db: bool):
        print("PSQL: Creating connection... ", end="")
        try:
            self.sqlconfig = ConfigSQL()
            self.connection = psycopg2.connect(
                database=os.getenv("DB_TEST_NAME") if is_test_db else os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PWD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            # self.connection = psycopg2.connect(
            #     database="test_postgres" if is_test_db else "postgres",
            #     user="postgres",
            #     password="postgres",
            #     host="postgres",
            #     port=5432
            # )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("DONE")
        except Exception as error:
            print("ERROR: ", error)

    def __del__(self):
        if self.connection:
            print("PSQL: Closing connection... ", end="")
            self.cursor.close()
            self.connection.close()
            print("DONE")

    def create_tables(self):
        print("PSQL: Start creating... ", end="")
        try:
            with open(self.sqlconfig.CREATE_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")

            print("PSQL: Start creating constraints... ", end="")
            with open(self.sqlconfig.CONSTRAINTS_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")
        except Exception as error:
            print("ERROR: ", error)

    def drop_tables(self):
        print("PSQL: Start dropping... ", end="")
        try:
            with open(self.sqlconfig.DROP_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")
        except Exception as error:
            print("ERROR: ", error)

    def copy_tables(self):
        print("PSQL: Start copying... ", end="")
        try:
            with open(self.sqlconfig.COPY_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")
        except Exception as error:
            print("ERROR: ", error)
