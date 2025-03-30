#!/bin/sh

set -e  # Stop on error

echo "Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI with Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
