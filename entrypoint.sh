#!/bin/sh

set -e

: "${DATABASE_HOSTNAME:=postgres}"
: "${DATABASE_PORT:=5432}"

echo "⏳ Waiting for PostgreSQL at $DATABASE_HOSTNAME:$DATABASE_PORT..."

while ! nc -z $DATABASE_HOSTNAME $DATABASE_PORT; do
  sleep 1
done

echo "✅ PostgreSQL is up and ready!"

echo "📦 Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
