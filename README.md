# AnimalsMD — Backend

A Flask REST API that helps pet owners figure out what might be wrong with their pet. Users register their pets, log symptoms, and get back possible illnesses, each with a description, home remedy, recommended medications, and products they can add to a cart.

I built this project to learn how to design and build RESTful APIs from the ground up: routing organized around resources, session authentication, database modeling, and the security concerns that come with handling real user accounts.

## What it does

- **Symptom-to-illness matching** — the core feature. A pet's symptoms and species classification are matched against a relational dataset of illnesses, so a coughing, sneezing dog gets back "respiratory infection" with treatment info, not a generic list.
- **Pet management** — full CRUD (Create, Read, Update, Delete) for pets, each tied to a species and a set of symptoms.
- **Shopping cart** — users add recommended products to a cart.
- **Session-based auth** — signup, login, logout, and session checks, with passwords hashed using Bcrypt.

## Technical highlights

- **Relational data model** — 16 SQLAlchemy models on PostgreSQL, including 6 many-to-many join tables (illness↔symptom, illness↔medication, illness↔product, species↔classification, and more) that power the diagnosis matching.
- **Security hardening** — CSRF (Cross-Site Request Forgery) protection via Flask-WTF with a token endpoint, rate limiting on login/signup with Flask-Limiter to block brute-force attempts, and thorough email validation with email-validator.
- **Serialization layer** — Marshmallow schemas keep API responses consistent and decoupled from the database models.
- **Database migrations** — schema changes are versioned with Flask-Migrate (Alembic).
- **Seed system** — a unified `seed.py` runner populates all 17 tables in dependency order, so you can seed a new database with one command.
- **Deployment-ready** — Gunicorn and a Procfile for production hosting.

## Documentation

- [api_endpoints.md](api_endpoints.md) — every endpoint with example requests and responses, split into public and auth-protected routes.
- [documentation.md](documentation.md) — local setup guide (pyenv, Pipenv, database, migrations).

## Tech stack

Python 3.8 · Flask · PostgreSQL · SQLAlchemy · Flask-Migrate · Marshmallow · Flask-WTF · Flask-Limiter · Bcrypt · Flask-CORS · Gunicorn
