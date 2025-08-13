import json
import os
from typing import Dict, Any, Optional

import boto3
import requests

from app.core.config import settings


def trigger_zap(payload: Dict[str, Any]) -> bool:
    if not settings.zapier_hook_url:
        return False
    try:
        resp = requests.post(settings.zapier_hook_url, json=payload, timeout=15)
        return 200 <= resp.status_code < 300
    except Exception:
        return False


def upload_file(content: bytes, key: str, content_type: str = "application/octet-stream") -> Optional[str]:
    if settings.storage_backend == "s3" and settings.s3_bucket:
        try:
            s3 = boto3.client(
                's3',
                region_name=settings.s3_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
            )
            s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=content, ContentType=content_type)
            return f"https://{settings.s3_bucket}.s3.{settings.s3_region}.amazonaws.com/{key}"
        except Exception:
            return None
    else:
        # local storage
        base = settings.local_storage_path
        os.makedirs(base, exist_ok=True)
        path = os.path.join(base, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
        return f"{settings.storage_base_url}/{key}"


def sync_events_to_google_sheets(rows: Dict[str, Any]) -> bool:
    # Placeholder: expects settings.google_service_account_json and google_sheets_id for real implementation
    # You can use gspread or Google Sheets API here.
    # This stub just returns True to indicate success.
    return True