#!/bin/sh

set -e

# Set default values if not provided
: "${DATABASE_HOSTNAME:=postgres}"
: "${DATABASE_PORT:=5432}"

echo "⏳ Waiting for PostgreSQL at $DATABASE_HOSTNAME:$DATABASE_PORT..."

# Wait until the DB is reachable
while ! nc -z "$DATABASE_HOSTNAME" "$DATABASE_PORT" >/dev/null 2>&1; do
  echo "⏱️  Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "✅ PostgreSQL is up and ready!"

echo "📦 Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
