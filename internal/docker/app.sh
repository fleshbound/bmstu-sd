#!/bin/bash

#alembic revision --autogenerate
#alembic upgrade head
cd /app/database/py && python3 setdb.py main

cd /app/src || exit 1
uvicorn app:app --host 0.0.0.0 --port ${APP_PORT}
