# Render deployment instructions

This file contains the exact steps to finish deploying this app to Render and the environment variables to set.

1. Merge the deploy-render branch into main (open PR: https://github.com/yashkansal12/Paper-Trading-using-AI-strategies/compare/main...deploy-render?expand=1).

2. (Recommended) Remove tracked SQLite DB from main after merging (BEFORE relying on production DB):
   - Back up any data you need.
   - Locally run:
     git checkout main
     git pull
     git rm --cached db.sqlite3
     echo "db.sqlite3" >> .gitignore
     git add .gitignore
     git commit -m "Remove tracked sqlite DB and ignore it"
     git push

3. Create a Render Web Service
   - Sign in to https://render.com and click New → Web Service → Connect a repository → GitHub → select this repository.
   - Branch: main (after you merge the PR)
   - Environment: Python
   - Build command:
     pip install -r requirements.txt && python manage.py collectstatic --noinput
   - Start command:
     bash -lc "python manage.py migrate --noinput && gunicorn config.wsgi"
   - Auto-deploy: enabled (optional)

4. Add Environment Variables in the Render Service settings
   - SECRET_KEY = <a secure random string>
   - DEBUG = False
   - ALLOWED_HOSTS = <optional, comma-separated hostnames>

5. Add a Managed Postgres Database (recommended)
   - In Render dashboard, create a new Managed Postgres instance.
   - Attach the database to your web service.
   - Render will set DATABASE_URL automatically; the app uses dj_database_url to pick it up.

6. After first deploy
   - Open the Render shell (Service → Shell) and run:
     python manage.py migrate
     python manage.py createsuperuser
   - Check logs for issues and fix any missing env vars or dependency errors.

Notes and tips
- The repo now includes runtime.txt pinning Python to 3.11.6; adjust if you prefer a different patch version.
- The repo contains render.yaml to help Render detect the service settings, but you still must connect the repo in Render and set secrets.
- I could not create the Render service on your account (requires your Render access).

If you want, I can:
- Walk you through the Render UI step-by-step while you create the service (I will tell you which buttons to press and what to paste).
- Add a GitHub Actions workflow or Dockerfile instead of Render.
