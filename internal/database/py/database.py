from dbconfig import DB_PWD, DB_HOST, DB_NAME, DB_USER, SQL_PATH
import psycopg2


class ConfigSQL:
    def __init__(self):
        self.CREATE_FILE = f"{SQL_PATH}/create_tables.sql"
        self.DROP_FILE = f"{SQL_PATH}/drop_tables.sql"
        self.COPY_FILE = f"{SQL_PATH}/copy_tables.sql"
        self.CONSTRAINTS_FILE = f"{SQL_PATH}/constraints.sql"


class DataBase:
    def __init__(self):
        print("PSQL: Creating connection... ", end="")
        try:
            self.sqlconfig = ConfigSQL()
            self.connection = psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PWD)
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
