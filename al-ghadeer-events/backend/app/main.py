from contextlib import asynccontextmanager
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.api.events import router as events_router
from app.api.tasks import router as tasks_router
from app.api.auth import router as auth_router
from app.api.payments import router as payments_router
from app.api.employees import router as employees_router
from app.api.expenses import router as expenses_router
from app.api.reports import router as reports_router
from app.api.integrations import router as integrations_router
from app.models.user import User

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Al Ghadeer Events Management System (FastAPI + PostgreSQL)...")

    # Seed admin user if not exists
    try:
        with SessionLocal() as db:  # type: Session
            admin = db.query(User).filter(User.email == settings.admin_email).first()
            if not admin:
                admin = User(
                    email=settings.admin_email,
                    username="admin",
                    full_name="System Administrator",
                    hashed_password=hash_password(settings.admin_password),
                    role="admin",
                    is_active=True,
                )
                db.add(admin)
                db.commit()
                logger.info("Admin user created")
    except Exception as e:
        logger.warning(f"Admin seed skipped: {e}")

    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Comprehensive event management system for Al Ghadeer Events",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Al Ghadeer Events Management System API",
        "version": settings.app_version,
        "status": "healthy",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": settings.app_version,
            "database": "connected",
            "environment": "production" if not settings.debug else "development",
        }
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e)})


# Routers
app.include_router(auth_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(payments_router, prefix="/api")
app.include_router(employees_router, prefix="/api")
app.include_router(expenses_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(integrations_router, prefix="/api")


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Resource not found"})


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )