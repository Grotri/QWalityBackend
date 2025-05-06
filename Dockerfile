FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    postgresql-client \
    postgresql \
    postgresql-contrib \
    build-essential \
    python3-dev \
    libc6-dev \
    postgresql-server-dev-all \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN if [ ! -d .git ]; then \
        git clone https://github.com/Grotri/QWalityBackend.git . && \
        git checkout develop; \
    else \
        git pull origin develop; \
    fi

RUN mkdir -p /var/run/postgresql && \
    chown -R postgres:postgres /var/run/postgresql && \
    mkdir -p /var/lib/postgresql/data && \
    chown -R postgres:postgres /var/lib/postgresql/data

COPY init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /var/lib/postgresql/data

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]