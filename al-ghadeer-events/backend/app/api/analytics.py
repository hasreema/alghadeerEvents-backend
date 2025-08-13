from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.event import Event

router = APIRouter(prefix="/analytics", tags=["Analytics"])()


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    query = db.query(Event)
    if start_date:
        query = query.filter(Event.date >= start_date)
    if end_date:
        query = query.filter(Event.date <= end_date)

    events = query.all()
    totals = {
        "events_count": len(events),
        "revenue": float(sum([e.payments_total or 0 for e in events])),
        "expenses": float(sum([e.expenses_total or 0 for e in events])),
        "labor": float(sum([e.labor_total or 0 for e in events])),
    }
    totals["profit"] = totals["revenue"] - totals["expenses"] - totals["labor"]
    return totals


@router.get("/profitability-by-type")
def profitability_by_type(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    rows = db.query(Event).all()
    grouped: Dict[str, Dict[str, float]] = {}
    for e in rows:
        key = e.event_type or "unknown"
        g = grouped.setdefault(key, {"revenue": 0.0, "expenses": 0.0, "labor": 0.0})
        g["revenue"] += float(e.payments_total or 0)
        g["expenses"] += float(e.expenses_total or 0)
        g["labor"] += float(e.labor_total or 0)
    result = []
    for k, v in grouped.items():
        profit = v["revenue"] - v["expenses"] - v["labor"]
        margin = (profit / v["revenue"] * 100.0) if v["revenue"] else 0.0
        result.append({"event_type": k, **v, "profit": profit, "margin": margin})
    return result


@router.get("/performance")
def performance(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    today = date.today()
    next_30 = db.query(Event).filter(Event.date >= today, Event.date <= today + timedelta(days=30)).count()
    overdue_outstanding = db.query(Event).filter(Event.outstanding_amount > 0).count()
    paid_events = db.query(Event).filter(Event.payment_status == "paid").count()
    return {
        "upcoming_30_days": next_30,
        "events_with_outstanding": overdue_outstanding,
        "paid_events": paid_events,
    }


@router.get("/alerts")
def alerts(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    # Simple alerts: unpaid events within next 7 days, high expense ratio
    today = date.today()
    soon = today + timedelta(days=7)
    unpaid_soon = db.query(Event).filter(Event.date >= today, Event.date <= soon, Event.payment_status != "paid").all()

    high_expense = []
    for e in db.query(Event).all():
        revenue = float(e.payments_total or 0)
        expenses = float(e.expenses_total or 0) + float(e.labor_total or 0)
        ratio = (expenses / revenue * 100.0) if revenue else 0.0
        if revenue and ratio > 70.0:
            high_expense.append({"id": e.id, "title": e.title, "expense_ratio": ratio})

    return {
        "unpaid_upcoming": [{"id": e.id, "title": e.title, "date": str(e.date)} for e in unpaid_soon],
        "high_expense_ratio": high_expense,
    }