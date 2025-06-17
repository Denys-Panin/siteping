FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src /src/

RUN mkdir -p /src/logs

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

