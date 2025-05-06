#!/bin/bash
set -e

if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw qwality; then
    sudo -u postgres createdb qwality
    echo "База данных 'qwality' создана."
else
    echo "База данных 'qwality' уже существует."
fi

export DATABASE_URL="postgresql://postgres@localhost:5432/qwality"
alembic upgrade head
python3 ./seeders/seed_tariffs.py