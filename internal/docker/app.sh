#!/bin/bash

alembic revision --autogenerate
alembic upgrade head
cd src || exit 1
uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}
