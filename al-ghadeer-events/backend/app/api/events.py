from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles, Pagination
from app.models.event import Event
from app.models.user import User
from app.schemas import EventCreate, EventUpdate, EventOut

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = Event(**payload.dict(), created_by=current_user.id, updated_by=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
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
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db.delete(event)
    db.commit()
    return None