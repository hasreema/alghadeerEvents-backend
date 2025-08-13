from pydantic import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    app_name: str = "Al Ghadeer Events API"
    app_version: str = "0.1.0"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # Database (psycopg v3)
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/alghadeer"

    # Frontend/CORS
    frontend_url: str = "http://localhost:5173"
    cors_origins: List[str] = []

    # Auth / JWT
    secret_key: str = "change-me-in-env"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 60 * 24

    # Optional admin seed
    admin_email: str = "admin@example.com"
    admin_password: str = "admin12345"

    # SMTP Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: Optional[str] = None
    smtp_use_tls: bool = True

    # WhatsApp (Twilio)
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_from_whatsapp: Optional[str] = None

    # Push (FCM)
    fcm_server_key: Optional[str] = None

    # Google Sheets
    google_service_account_json: Optional[str] = None
    google_sheets_id: Optional[str] = None

    # Zapier
    zapier_hook_url: Optional[str] = None

    # Storage
    storage_backend: str = "local"  # local | s3
    storage_base_url: str = "http://localhost:8000/files"  # for local downloads, adjust behind proxy
    local_storage_path: str = "storage"
    s3_bucket: Optional[str] = None
    s3_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # Reporting
    hebrew_font_path: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        origins_env = os.getenv("CORS_ORIGINS")
        if not self.cors_origins:
            if origins_env:
                self.cors_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
            else:
                self.cors_origins = [
                    self.frontend_url,
                    "http://localhost:3000",
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "http://127.0.0.1:3000",
                ]


settings = Settings()