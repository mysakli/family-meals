FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build-time collectstatic (runtime DB not required; WhiteNoise serves STATIC_ROOT)
ENV SECRET_KEY=build-only \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    USE_S3=False
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "FamilyMeals.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
