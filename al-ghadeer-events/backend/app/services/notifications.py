import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth

from app.core.config import settings


def send_email(subject: str, body_html: str, to_emails: List[str], body_text: Optional[str] = None) -> bool:
    if not settings.smtp_host or not settings.smtp_from:
        return False
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.smtp_from
    msg['To'] = ", ".join(to_emails)

    if body_text:
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_user and settings.smtp_password:
            server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_from, to_emails, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


def send_whatsapp(message: str, to_number: str) -> bool:
    if not settings.twilio_account_sid or not settings.twilio_auth_token or not settings.twilio_from_whatsapp:
        return False
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json"
    data = {
        'From': f"whatsapp:{settings.twilio_from_whatsapp}",
        'To': f"whatsapp:{to_number}",
        'Body': message,
    }
    try:
        resp = requests.post(url, data=data, auth=HTTPBasicAuth(settings.twilio_account_sid, settings.twilio_auth_token), timeout=15)
        return 200 <= resp.status_code < 300
    except Exception:
        return False


def send_push(title: str, body: str, device_token: str) -> bool:
    if not settings.fcm_server_key:
        return False
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={settings.fcm_server_key}',
    }
    payload = {
        'to': device_token,
        'notification': {'title': title, 'body': body},
    }
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        return 200 <= resp.status_code < 300
    except Exception:
        return False