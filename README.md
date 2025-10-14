# Family Meals

A simple Django app to manage family meals.

## Quick start (development)

1. Create and activate a virtual environment (if you don't already have the project's venv):

```bash
python3 -m venv venv
source venv/bin/activate
```

(If you've already created `venv_meals`, activate it instead:)

```bash
source /home/michaela/Dokumenty/Coding/meals/venv_meals/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

To capture exact pinned versions from the project's existing virtualenv run:

```bash
/home/michaela/Dokumenty/Coding/meals/venv_meals/bin/python -m pip freeze > requirements.txt
```

3. Environment variables

The project reads configuration from environment variables (via `python-dotenv`). Create a `.env` in the project root containing at least:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

4. Database migrations

```bash
python manage.py migrate
```

5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

6. Run the development server

```bash
python manage.py runserver
```

7. Media and static files

- Media files are served from `MEDIA_ROOT` (`media/` by default).
- Static files are collected from `entries/static` in development.

## Notes

- `settings.py` shows the project was generated with Django 5.1; adjust `requirements.txt` if you need a different Django version.
- The project uses PostgreSQL in `settings.py`. If you want to use the included sqlite DB for quick testing, edit `FamilyMeals/settings.py` or set the DB env vars accordingly.

## Troubleshooting

- If you see missing packages, install them via `pip install <package>` and re-run `pip freeze` to update `requirements.txt`.
- For image processing, ensure `Pillow` is installed.

---

If you'd like, I can also:
- Pin exact package versions by running `pip freeze` in your `venv_meals`.
- Add simple unit test commands or CI config (GitHub Actions) to run tests automatically.