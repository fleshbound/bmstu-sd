from urllib.parse import urlparse  # for python 3+ use: from urllib.parse import urlparse
from typing import Any

from dbconfig import DB_PWD, DB_HOST, DB_NAME, DB_USER, SQL_PATH, DB_PORT, DB_TEST_NAME
import psycopg2


class ConfigSQL:
    def __init__(self):
        self.CREATE_FILE = f"{SQL_PATH}/create_tables.sql"
        self.DROP_FILE = f"{SQL_PATH}/drop_tables.sql"
        self.COPY_FILE = f"{SQL_PATH}/copy_tables.sql"
        self.CONSTRAINTS_FILE = f"{SQL_PATH}/constraints.sql"


class Database:
    connection: Any
    cursor: Any

    def __init__(self):
        print("PSQL: Creating connection... ", end="")
        try:
            self.sqlconfig = ConfigSQL()
            result = urlparse(f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}")
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            port = result.port
            self.connection = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("DONE")
        except Exception as error:
            print("ERROR (", error, ")")

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
            print("ERROR (", error, ")")

    def drop_tables(self):
        print("PSQL: Start dropping... ", end="")
        try:
            with open(self.sqlconfig.DROP_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")
        except Exception as error:
            print("ERROR (", error, ")")

    def copy_tables(self):
        print("PSQL: Start copying... ", end="")
        try:
            with open(self.sqlconfig.COPY_FILE, "r") as f:
                self.cursor.execute(f.read())
            print("DONE")
        except Exception as error:
            print("ERROR (", error, ")")
