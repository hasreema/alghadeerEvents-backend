from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel


# ----------------------
# Event Schemas
# ----------------------
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    date: date
    time: Optional[time] = None
    organizer: Optional[str] = None
    status: Optional[str] = "scheduled"


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    organizer: Optional[str] = None
    status: Optional[str] = None


class EventOut(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ----------------------
# Task Schemas
# ----------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "normal"
    event_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    event_id: Optional[int] = None


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True