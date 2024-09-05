import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TestConfigs(BaseSettings):
    # database
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    #
    # POSTGRES_DB: str = 'postgres'
    # POSTGRES_PORT: str = '5432'
    # POSTGRES_USER: str = 'postgres'
    # POSTGRES_PASSWORD: str = 'postgres'

    DATABASE_URL: str = "postgresql://{user}:{password}@postgres:{port}/{database}".format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )

    class Config:
        case_sensitive = True


configs = Configs()
