from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles, Pagination
from app.models.event import Event
from app.models.user import User
from app.models.event_extras import EventService, EventContact, EventAssignment
from app.schemas import EventCreate, EventUpdate, EventOut, EventServiceCreate, EventContactCreate, EventAssignmentCreate
from app.services.finance import recalc_event_financials

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = Event(**payload.dict(), created_by=current_user.id, updated_by=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    recalc_event_financials(db, event.id)
    return event


@router.get("/", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: Pagination = Depends(),
    status_filter: Optional[str] = Query(None, alias="status"),
    location: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    search: Optional[str] = Query(None, description="Search in title"),
):
    query = db.query(Event)
    if status_filter:
        query = query.filter(Event.status == status_filter)
    if location:
        query = query.filter(Event.location == location)
    if start_date:
        query = query.filter(Event.date >= start_date)
    if end_date:
        query = query.filter(Event.date <= end_date)
    if search:
        like = f"%{search}%"
        query = query.filter(Event.title.ilike(like))

    return query.order_by(Event.date.desc()).offset(pagination.offset).limit(pagination.limit).all()


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    event.updated_by = current_user.id

    db.add(event)
    db.commit()
    db.refresh(event)
    recalc_event_financials(db, event.id)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db.delete(event)
    db.commit()
    return None


# Services management
@router.post("/{event_id}/services", status_code=status.HTTP_201_CREATED)
def add_service(event_id: int, body: EventServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    total_price = body.quantity * body.unit_price
    service = EventService(event_id=event_id, name=body.name, quantity=body.quantity, unit_price=body.unit_price, total_price=total_price)
    db.add(service)
    db.commit()
    recalc_event_financials(db, event_id)
    return {"id": service.id}


@router.delete("/{event_id}/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_service(event_id: int, service_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = db.query(EventService).filter(EventService.id == service_id, EventService.event_id == event_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    recalc_event_financials(db, event_id)
    return None


# Contacts management
@router.post("/{event_id}/contacts", status_code=status.HTTP_201_CREATED)
def add_contact(event_id: int, body: EventContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    contact = EventContact(event_id=event_id, name=body.name, phone=body.phone, email=body.email, note=body.note)
    db.add(contact)
    db.commit()
    return {"id": contact.id}


@router.delete("/{event_id}/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_contact(event_id: int, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(EventContact).filter(EventContact.id == contact_id, EventContact.event_id == event_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return None


# Assignments (labor)
@router.post("/{event_id}/assignments", status_code=status.HTTP_201_CREATED)
def add_assignment(event_id: int, body: EventAssignmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    total_cost = body.hours * body.hourly_rate
    assignment = EventAssignment(event_id=event_id, employee_id=body.employee_id, role=body.role, hours=body.hours, hourly_rate=body.hourly_rate, total_cost=total_cost)
    db.add(assignment)
    db.commit()
    recalc_event_financials(db, event_id)
    return {"id": assignment.id}


@router.delete("/{event_id}/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_assignment(event_id: int, assignment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignment = db.query(EventAssignment).filter(EventAssignment.id == assignment_id, EventAssignment.event_id == event_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    recalc_event_financials(db, event_id)
    return None