FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    postgresql-client \
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

COPY init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]