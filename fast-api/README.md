# Eleven Labs Demo App

This project structure aims to be MVP for a fast api app with phone calling via twillio using eleven labs for speech.
It can be run locally or easily deployed to any infrastructure provider just by swapping out .env vars.

## Project Structure / Moving Pieces

Database - Postgres
Web Framework - Fast API
Phone Infra - Twilio
Voice/Speach - Eleven Labs

### Application Structure

app/ - Entire Fast API Application
/app/main.py - Entrypoint and router setup
/app/database.py - DB config
/app/dependencies.py - Dependency injection for services & repositories
/app/models.py - (SQLModel)[https://sqlmodel.tiangolo.com/] ORM models
/app/routers - API routes
/app/repositories - DB calls
/app/services - Business logic

# Getting Started

## Replit

1. Pull the repo into replit
2. Create the database, grab the `DATABASE_URL`
3. Add replit secrets for `ELEVENLABS_API_KEY`, `ELEVENLABS_AGENT_ID`, `DATABASE_URL` and `ADMIN_SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`
4. Click Run
5. Open the web browser and head to /health-check. You should see {"status":"up","database_check":false}. It will be false for now because you have not yet run a migration.
6. Execute the sql in migrations/001.sql
7. Check `/health-check` again and confirm that you now see {"status":"up","database_check":true}.
8. Set twilio callback to the replit url

## Local

Make sure you have python3.11 installed and docker desktop running

1. python3.11 -m venv venv
2. source venv/bin/activate
3. Create .env and make sure you have values for `ELEVENLABS_API_KEY`, `ELEVENLABS_AGENT_ID` and `ADMIN_SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`. `DATABASE_URL` will be postgresql://eleven_demo_local_user:eleven_demo_local_password@db:5432/eleven_demo_local_db from our docker setup.
4. `make run`
5. Head to localhost:8000/health-check and you should see {"status":"up","database_check":true}

### Ngrok - Optional

1. Create an ngrok account and grab your static url
2. Add NGROK_STATIC_URL to .env with your value
3. Run `make ngrok`, and use this url with twilio.

# Helpful Utils

`make verify_types` runs mypy type checking.

# Admin Dashboard

We have an admin dashboard using (SQL ADMIN)[https://aminalaee.dev/sqladmin/].

Make sure to add the env vars for `ADMIN_SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` and then:

1. `make run`
2. Head to localhost:8000/admin and login
3. View data
