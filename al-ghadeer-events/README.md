# Al Ghadeer Events – Backend (FastAPI + PostgreSQL)

This backend provides Events and Tasks CRUD with optional linkage of tasks to events, plus JWT authentication and RBAC foundation. It exposes OpenAPI docs, uses PostgreSQL via SQLAlchemy, and ships with Alembic migrations and Docker Compose.

## Quick start (Docker)

1. Copy the example env file and adjust if needed:

```bash
cp backend/.env.example backend/.env
```

2. Start Postgres and the API:

```bash
docker compose up -d --build
```

3. Open docs:

- API root: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs

## Configuration

- `backend/app/core/config.py` reads environment variables from `backend/.env`:
  - `DATABASE_URL` (default: `postgresql+psycopg2://postgres:postgres@db:5432/alghadeer`)
  - `FRONTEND_URL` and `CORS_ORIGINS` for CORS
  - `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRES_MINUTES`
  - `ADMIN_EMAIL`, `ADMIN_PASSWORD` for seeding admin on startup
  - `PORT`, `HOST`, `DEBUG`

## Alembic migrations

- Migrations are applied automatically on container start (`backend/start.sh`).
- To run manually (with Python env activated):

```bash
cd backend
alembic upgrade head
```

## Authentication

- Register: `POST /api/auth/register` with JSON body `{ email, username?, full_name?, role?, password }`
- Login: `POST /api/auth/login` with form body `username=<email>&password=<password>`
- Current user: `GET /api/auth/me` with `Authorization: Bearer <token>`

Use the returned bearer token to access protected endpoints.

## Endpoints

- `POST /api/events` – Create event (auth required)
- `GET /api/events` – List events (auth required)
- `GET /api/events/{id}` – Get event (auth required)
- `PUT /api/events/{id}` – Update event (auth required)
- `DELETE /api/events/{id}` – Delete event (auth required)

- `POST /api/tasks` – Create task (auth required)
- `GET /api/tasks` – List tasks (auth required; optional `?event_id=`)
- `GET /api/tasks/{id}` – Get task (auth required)
- `PUT /api/tasks/{id}` – Update task (auth required)
- `DELETE /api/tasks/{id}` – Delete task (auth required)

## Notes

- Extend models/routers to cover more modules (payments, employees, expenses, reminders, reports) next.
- Multi-language, Google Sheets, WhatsApp, and PDF reporting will follow in later phases.