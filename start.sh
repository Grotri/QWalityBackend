#!/bin/bash

until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

export PGPASSWORD=postgres

psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'qwality'" | grep -q 1 || psql -h db -U postgres -c "CREATE DATABASE qwality"

export SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@db:5432/qwality"

alembic upgrade head

export PYTHONPATH=/app:$PYTHONPATH

python ./seeders/seed_tariffs.py

flask run --host=0.0.0.0