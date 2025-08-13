#!/usr/bin/env bash
set -euo pipefail

# Run DB migrations
python -m alembic upgrade head

# Start FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
