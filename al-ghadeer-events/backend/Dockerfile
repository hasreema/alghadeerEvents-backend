FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies + dos2unix
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app & alembic
COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic
COPY start.sh ./

# Force start.sh to Unix format + make executable
RUN dos2unix /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
