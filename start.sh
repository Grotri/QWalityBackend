#!/bin/bash
set -e

su postgres -c "pg_ctlcluster 13 main start"

until pg_isready -h localhost; do
  sleep 1
done

if [ -f /docker-entrypoint-initdb.d/init_db.sh ]; then
    /docker-entrypoint-initdb.d/init_db.sh
fi

exec flask run --host=0.0.0.0