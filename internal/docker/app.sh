#!/bin/bash

#alembic revision --autogenerate
#alembic upgrade head
cd /app/database/py && python3 setdb.py main

cd /app/src || exit 1
uvicorn app:app --host localhost --port ${APP_PORT}
