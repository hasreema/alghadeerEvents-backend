from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import String

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles, Pagination
from app.models.event import Event
from app.models.user import User
from app.models.event_extras import EventService, EventContact, EventAssignment
from app.schemas import (
    PaginatedResponse,
    EventContractCreate, EventContractUpdate, EventResponse,
    EventServiceCreate, EventContactCreate, EventAssignmentCreate,
)
from app.services.finance import recalc_event_financials

router = APIRouter(prefix="/events", tags=["Events"])


def to_response(e: Event) -> EventResponse:
    outstanding = float(e.outstanding_amount or 0)
    total_rev = float(e.quoted_total or 0)
    total_exp = float(e.expenses_total or 0)
    labor = float(e.labor_total or 0)
    profit = total_rev - total_exp - labor
    margin = (profit / total_rev * 100.0) if total_rev else 0.0
    return EventResponse(
        id=e.id,
        event_name=e.name or e.title,
        event_type=e.type or e.event_type or "",
        event_type_other=e.type_custom,
        location=", ".join(e.locations or []) if e.locations else (e.location or ""),
        status=e.status,
        event_date=e.starts_at or datetime.combine(e.date, e.time or datetime.min.time()),
        start_time=(e.time.strftime("%H:%M") if e.time else None),
        end_time=(e.end_time.strftime("%H:%M") if e.end_time else None),
        expected_guests=e.guest_count,
        actual_guests=e.actual_guests,
        guest_gender=e.gender,
        contacts=e.contacts_json,
        services=e.services_flags,
        special_requests=e.special_requests_text,
        pricing=e.pricing,
        payment_status=e.payment_status,
        deposit_amount=float(e.deposit_total or 0),
        deposit_paid=bool(e.deposit_paid_flag) if e.deposit_paid_flag is not None else None,
        outstanding_balance=outstanding,
        assigned_employees=[],
        labor_cost=float(e.labor_total or 0),
        total_revenue=float(e.quoted_total or 0),
        total_expenses=float(e.expenses_total or 0),
        profit=profit,
        profit_margin=margin,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


@router.get("/", response_model=PaginatedResponse)
def list_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: Pagination = Depends(),
    status: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    q = db.query(Event)
    if status:
        q = q.filter(Event.status == status)
    if event_type:
        q = q.filter((Event.type == event_type) | (Event.event_type == event_type))
    if location:
        q = q.filter((Event.locations.cast(String).ilike(f"%{location}%")) | (Event.location == location))
    if search:
        like = f"%{search}%"
        q = q.filter((Event.name.ilike(like)) | (Event.title.ilike(like)))
    if start_date:
        q = q.filter(Event.date >= start_date)
    if end_date:
        q = q.filter(Event.date <= end_date)

    total = q.count()
    items = q.order_by(Event.date.desc()).offset(pagination.offset).limit(pagination.limit).all()
    return {
        "items": [to_response(e) for e in items],
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
        "total_pages": (total + pagination.page_size - 1) // pagination.page_size,
    }


@router.get("/upcoming", response_model=List[EventResponse])
def upcoming(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = Query(10, ge=1, le=50)):
    today = datetime.utcnow()
    rows = db.query(Event).filter(Event.status != "cancelled", Event.date >= today.date()).order_by(Event.date.asc()).limit(limit).all()
    return [to_response(e) for e in rows]


@router.get("/stats/overview")
def stats_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), start_date: Optional[date] = Query(None), end_date: Optional[date] = Query(None)):
    q = db.query(Event)
    if start_date:
        q = q.filter(Event.date >= start_date)
    if end_date:
        q = q.filter(Event.date <= end_date)
    events = q.all()
    total_events = len(events)
    total_revenue = sum(float(e.quoted_total or 0) for e in events)
    total_expenses = sum(float(e.expenses_total or 0) for e in events)
    total_profit = total_revenue - total_expenses - sum(float(e.labor_total or 0) for e in events)
    avg_margin = (sum(((float(e.quoted_total or 0) - float(e.expenses_total or 0) - float(e.labor_total or 0)) / float(e.quoted_total or 1) * 100.0) for e in events if float(e.quoted_total or 0) > 0) / total_events) if total_events else 0
    status_breakdown = {}
    type_breakdown = {}
    upcoming_events = len([e for e in events if (e.date or datetime.min.date()) >= datetime.utcnow().date() and e.status != "cancelled"])
    for e in events:
        status_breakdown[e.status or "unknown"] = status_breakdown.get(e.status or "unknown", 0) + 1
        etype = e.type or e.event_type or "unknown"
        type_breakdown[etype] = type_breakdown.get(etype, 0) + 1
    return {
        "total_events": total_events,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "average_profit_margin": avg_margin,
        "status_breakdown": status_breakdown,
        "type_breakdown": type_breakdown,
        "upcoming_events": upcoming_events,
    }


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return to_response(e)


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event_contract(payload: EventContractCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = Event(
        name=payload.event_name,
        type=payload.event_type,
        type_custom=payload.event_type_other,
        starts_at=payload.event_date,
        date=payload.event_date.date(),
        time=datetime.strptime(payload.start_time, "%H:%M").time() if payload.start_time else None,
        end_time=datetime.strptime(payload.end_time, "%H:%M").time() if payload.end_time else None,
        locations=[s.strip() for s in (payload.location or "").split(",") if s.strip()],
        guest_count=payload.expected_guests,
        gender=payload.guest_gender,
        contacts_json=[c.dict() for c in (payload.contacts or [])],
        services_flags=payload.services,
        special_requests_text=payload.special_requests,
        decoration_type=payload.decoration_type,
        menu_selections=payload.menu_selections,
        dietary_restrictions=payload.dietary_restrictions,
        pricing=payload.pricing,
        deposit_total=payload.deposit_amount,
        internal_notes=payload.internal_notes,
        title=payload.event_name,
        event_type=payload.event_type,
        status="pending",
        created_by=current_user.id,
        updated_by=current_user.id,
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    recalc_event_financials(db, e.id)
    return to_response(e)


@router.put("/{event_id}", response_model=EventResponse)
def update_event_contract(event_id: int, payload: EventContractUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")

    data = payload.dict(exclude_unset=True)
    if "event_name" in data:
        e.name = data["event_name"]; e.title = data["event_name"]
    if "event_type" in data:
        e.type = data["event_type"]; e.event_type = data["event_type"]
    if "event_type_other" in data:
        e.type_custom = data["event_type_other"]
    if "event_date" in data:
        e.starts_at = data["event_date"]; e.date = data["event_date"].date(); e.time = (e.time or datetime.min.time())
    if "start_time" in data and data["start_time"]:
        e.time = datetime.strptime(data["start_time"], "%H:%M").time()
    if "end_time" in data and data["end_time"]:
        e.end_time = datetime.strptime(data["end_time"], "%H:%M").time()
    if "location" in data:
        e.locations = [s.strip() for s in data["location"].split(",") if s.strip()]
    if "expected_guests" in data:
        e.guest_count = data["expected_guests"]
    if "guest_gender" in data:
        e.gender = data["guest_gender"]
    if "contacts" in data:
        e.contacts_json = [c.dict() for c in (data["contacts"] or [])]
    if "services" in data:
        e.services_flags = data["services"]
    if "special_requests" in data:
        e.special_requests_text = data["special_requests"]
    if "decoration_type" in data:
        e.decoration_type = data["decoration_type"]
    if "menu_selections" in data:
        e.menu_selections = data["menu_selections"]
    if "dietary_restrictions" in data:
        e.dietary_restrictions = data["dietary_restrictions"]
    if "pricing" in data:
        e.pricing = data["pricing"]; e.quoted_total = float((data["pricing"] or {}).get("total_price", e.quoted_total or 0))
    if "deposit_amount" in data:
        e.deposit_total = data["deposit_amount"]
    if "internal_notes" in data:
        e.internal_notes = data["internal_notes"]

    e.updated_by = current_user.id
    db.add(e)
    db.commit()
    db.refresh(e)
    recalc_event_financials(db, e.id)
    return to_response(e)


@router.post("/{event_id}/cancel", response_model=EventResponse)
def cancel_event(event_id: int, reason: Optional[str] = Body(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    e.status = "cancelled"
    e.cancel_reason = reason
    e.updated_by = current_user.id
    db.add(e)
    db.commit()
    db.refresh(e)
    return to_response(e)


@router.post("/{event_id}/assign-employees", response_model=EventResponse)
def assign_employees(event_id: int, employee_ids: List[str], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    # Placeholder: store in internal_notes for now or add a specific JSONB field
    e.internal_notes = (e.internal_notes or "") + f"\nAssigned: {', '.join(employee_ids)}"
    e.updated_by = current_user.id
    db.add(e)
    db.commit()
    db.refresh(e)
    return to_response(e)


@router.delete("/{event_id}", response_model=dict, dependencies=[Depends(require_roles(["admin"]))])
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    e = db.query(Event).filter(Event.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(e)
    db.commit()
    return {"message": "Event deleted successfully"}