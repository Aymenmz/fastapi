#!/bin/sh

set -e  # Stop on error

: "${DATABASE_HOSTNAME:=postgres}"
: "${DATABASE_PORT:=5432}"

echo "waiting for PostgreSQL to be ready..."
while ! nc -z $DATABASE_HOSTNAME $DATABASE_PORT;
  sleep 1
done
echo "PostgreSQL is up and ready!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI with Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
