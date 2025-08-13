from pydantic import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    app_name: str = "Al Ghadeer Events API"
    app_version: str = "0.1.0"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/alghadeer"

    # Frontend/CORS
    frontend_url: str = "http://localhost:5173"
    cors_origins: List[str] = []

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Allow comma-separated list from env
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