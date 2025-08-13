# Al Ghadeer Events – Backend (FastAPI + PostgreSQL)

This backend provides Events and Tasks CRUD with optional linkage of tasks to events, plus JWT authentication and RBAC foundation. It exposes OpenAPI docs, uses PostgreSQL via SQLAlchemy, and ships with Alembic migrations and Docker Compose.

Note: Use Docker for running locally to avoid host Python version/package compatibility issues.

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
  - `DATABASE_URL` (default: `postgresql+psycopg://postgres:postgres@db:5432/alghadeer`)
  - `FRONTEND_URL` and `CORS_ORIGINS` for CORS
  - `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRES_MINUTES`
  - `ADMIN_EMAIL`, `ADMIN_PASSWORD` for seeding admin on startup
  - `PORT`, `HOST`, `DEBUG`

## Alembic migrations

- Migrations are applied automatically on container start (`backend/start.sh`).
- To run manually:

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

- Events (auth required)
  - `POST /api/events`
  - `GET /api/events`
  - `GET /api/events/{id}`
  - `PUT /api/events/{id}`
  - `DELETE /api/events/{id}`

- Tasks (auth required)
  - `POST /api/tasks`
  - `GET /api/tasks[?event_id=]`
  - `GET /api/tasks/{id}`
  - `PUT /api/tasks/{id}`
  - `DELETE /api/tasks/{id}`

- Payments (auth required)
  - `POST /api/payments`
  - `GET /api/payments`
  - `GET /api/payments/{id}`
  - `PUT /api/payments/{id}`
  - `DELETE /api/payments/{id}`

- Expenses (auth required)
  - `POST /api/expenses`
  - `GET /api/expenses`
  - `GET /api/expenses/{id}`
  - `PUT /api/expenses/{id}`
  - `DELETE /api/expenses/{id}`

- Employees (auth required; admin to create/update/delete)
  - `POST /api/employees`
  - `GET /api/employees`
  - `GET /api/employees/{id}`
  - `PUT /api/employees/{id}`
  - `DELETE /api/employees/{id}`

## Notes

- Extend models/routers to cover richer business logic (profitability, status workflows, contacts) next.
- Multi-language, Google Sheets, WhatsApp, and PDF reporting will follow in later phases.