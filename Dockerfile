FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY="build-only-placeholder-not-used-in-production"

RUN python manage.py collectstatic --noinput

CMD exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2