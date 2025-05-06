#!/bin/bash
set -e

if [ ! -d "/var/lib/postgresql/data/pgdata" ]; then
    sudo -u postgres initdb -D /var/lib/postgresql/data/pgdata
fi

sudo -u postgres pg_ctl -D /var/lib/postgresql/data/pgdata -l /var/log/postgresql.log start

until sudo -u postgres pg_isready; do
    sleep 1
done

if [ -f /docker-entrypoint-initdb.d/init_db.sh ]; then
    /docker-entrypoint-initdb.d/init_db.sh
fi

exec flask run --host=0.0.0.0