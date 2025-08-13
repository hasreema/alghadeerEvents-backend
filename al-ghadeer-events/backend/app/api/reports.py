from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.event import Event
from app.services.reports import generate_monthly_pdf, export_events_excel

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly/pdf")
def monthly_pdf(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    events = db.query(Event).filter(Event.date >= date(year, month, 1)).all()
    month_label = f"{month:02d}/{year}"
    pdf_bytes = generate_monthly_pdf(events, month_label)
    return StreamingResponse(iter([pdf_bytes]), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=monthly_{year}_{month:02d}.pdf"
    })


@router.get("/events.xlsx")
def events_excel(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    events = db.query(Event).order_by(Event.date.desc()).all()
    xlsx = export_events_excel(events)
    return StreamingResponse(iter([xlsx]), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
        "Content-Disposition": "attachment; filename=events.xlsx"
    })