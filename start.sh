#!/bin/bash

until pg_isready -h localhost -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

psql -h localhost -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'qwality'" | grep -q 1 || psql -h localhost -U postgres -c "CREATE DATABASE qwality"

alembic upgrade head

export PYTHONPATH=/app:$PYTHONPATH

python ./seeders/seed_tariffs.py

flask run --host=0.0.0.0