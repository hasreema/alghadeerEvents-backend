import os
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "healthy"


def test_auth_register_and_login(monkeypatch):
    # Skip actual DB usage in this skeleton; ensure endpoints exist
    assert app.openapi_url == "/openapi.json"
    # Endpoints available
    for path, method in [
        ("/api/auth/register", "post"),
        ("/api/auth/login", "post"),
    ]:
        assert any(r.path == path for r in app.routes)