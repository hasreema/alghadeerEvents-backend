#!/usr/bin/env bash
set -euo pipefail

# Run DB migrations
alembic upgrade head

# Start the app
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}