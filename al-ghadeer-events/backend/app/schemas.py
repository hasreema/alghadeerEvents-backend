from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ----------------------
# User Schemas
# ----------------------
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = Field(default="staff", pattern="^(admin|staff)$")


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

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
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True


# ----------------------
# Payment Schemas
# ----------------------
class PaymentBase(BaseModel):
    event_id: int
    amount: float
    method: Optional[str] = None
    status: Optional[str] = "paid"
    note: Optional[str] = None
    receipt_url: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    event_id: Optional[int] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None
    receipt_url: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentOut(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True