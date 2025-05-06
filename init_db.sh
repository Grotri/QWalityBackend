#!/bin/bash
set -e

if ! psql -U postgres -h postgres -lqt | cut -d \| -f 1 | grep -qw qwality; then
    psql -U postgres -h postgres -c "CREATE DATABASE qwality;"
    echo "База данных 'qwality' создана."
else
    echo "База данных 'qwality' уже существует."

alembic upgrade head
python3 ./seeders/seed_tariffs.py

fi