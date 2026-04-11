# Technology Stack: Family Meals

## Core Infrastructure

- **Language**: Python (v3.x)
- **Backend Framework**: Django (v5.1)
- **Database**: PostgreSQL (primary), SQLite (dev)
- **Storage**: AWS S3 (via `django-storages` and `boto3`)

## Frontend Architecture

- **Primary CSS Framework**: Tailwind CSS (Utility-first approach)
- **Legacy Framework**: None (Bootstrap 5 removed)
- **Template Engine**: Django Templates

## Tooling & Deployment

- **WSGI Server**: Gunicorn
- **Static File Handling**: Whitenoise
- **Configuration**: `python-dotenv` and `dj-database-url` (Render/Heroku-compatible)
- **Image Processing**: Pillow (Automatic resizing/cropping)
