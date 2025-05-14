FROM python:3.10

RUN apt-get update && \
    apt-get install -y libgl1-mesa-dev libglib2.0-0 && \
    apt-get install ffmpeg libsm6 libxext6 -y && \
    apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    postgresql \
    postgresql-client \
    postgresql-contrib \
    build-essential \
    python3-dev \
    libc6-dev \
    gcc \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Grotri/QWalityBackend.git /app
WORKDIR /app
RUN git checkout develop

RUN pip install -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]