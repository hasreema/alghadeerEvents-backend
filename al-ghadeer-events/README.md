# Al Ghadeer Events – Backend (FastAPI + PostgreSQL)

This backend provides Events and Tasks CRUD with optional linkage of tasks to events. It exposes OpenAPI docs, uses PostgreSQL via SQLAlchemy, and ships with Alembic migrations and Docker Compose.

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
  - `PORT`, `HOST`, `DEBUG`

## Alembic migrations

- Migrations are applied automatically on container start (`backend/start.sh`).
- To run manually (with Python env activated):

```bash
cd backend
alembic upgrade head
```

## Endpoints

- `POST /api/events` – Create event
- `GET /api/events` – List events
- `GET /api/events/{id}` – Get event
- `PUT /api/events/{id}` – Update event
- `DELETE /api/events/{id}` – Delete event

- `POST /api/tasks` – Create task (optional `event_id`)
- `GET /api/tasks` – List tasks (optional `?event_id=`)
- `GET /api/tasks/{id}` – Get task
- `PUT /api/tasks/{id}` – Update task
- `DELETE /api/tasks/{id}` – Delete task

## Notes

- This service is intended for internal staff usage and integrates with a mobile-first UI.
- Extend models/routers to cover more modules (payments, employees, etc.) as needed.