# LifeLink

LifeLink is a Django-based blood bank management system.

## Initial setup

1. Activate the virtual environment and install dependencies:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set `DJANGO_SECRET_KEY` to a generated value, for example:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   For production, keep the key private, turn off `DJANGO_DEBUG`, and set `DJANGO_ALLOWED_HOSTS`.
3. Keep `DB_ENGINE=sqlite` for local development, or use `DB_ENGINE=mysql` and configure the database variables after creating the database in XAMPP. Django 6.1 requires MySQL 8.4+ or MariaDB 10.11+; verify the XAMPP server version before switching.
4. Create and apply migrations:

   ```powershell
   python manage.py makemigrations accounts
   python manage.py migrate
   python manage.py test
   ```

The custom `accounts.User` model is configured before the initial migration. Do not migrate with Django's default user model first.

## Donor and hospital profiles

After signing in, donor users can create or update their profile at `/donors/profile/`, and hospital users can do the same at `/hospitals/profile/`. Other roles are denied access. Hospital verification is managed by an administrator and cannot be set through the hospital profile form.
