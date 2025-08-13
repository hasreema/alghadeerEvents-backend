from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_roles
from app.services.notifications import send_email, send_whatsapp, send_push
from app.services.integrations import trigger_zap, sync_events_to_google_sheets

router = APIRouter(prefix="/integrations", tags=["Integrations"])


@router.post("/notify/email")
def notify_email(subject: str, body_html: str, to_emails: List[str], _: str = Depends(get_current_user)):
    ok = send_email(subject, body_html, to_emails)
    return {"success": ok}


@router.post("/notify/whatsapp")
def notify_whatsapp(message: str, to_number: str, _: str = Depends(get_current_user)):
    ok = send_whatsapp(message, to_number)
    return {"success": ok}


@router.post("/notify/push")
def notify_push(title: str, body: str, device_token: str, _: str = Depends(get_current_user)):
    ok = send_push(title, body, device_token)
    return {"success": ok}


@router.post("/zapier")
def zapier(payload: Dict[str, Any], _: str = Depends(get_current_user)):
    ok = trigger_zap(payload)
    return {"success": ok}


@router.post("/google-sheets/sync")
def google_sheets_sync(payload: Dict[str, Any], _: str = Depends(get_current_user)):
    ok = sync_events_to_google_sheets(payload)
    return {"success": ok}