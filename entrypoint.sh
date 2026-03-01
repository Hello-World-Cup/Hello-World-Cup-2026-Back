#!/bin/sh

echo "Running migrations..."
alembic upgrade head

echo "Starting container CMD..."
exec "$@"