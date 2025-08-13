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
# Employee Schemas
# ----------------------
class EmployeeBase(BaseModel):
    full_name: str
    role: Optional[str] = None
    hourly_wage: Optional[float] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    hourly_wage: Optional[float] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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
    status: Optional[str] = "draft"
    event_type: Optional[str] = None
    quoted_total: Optional[float] = 0


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
    event_type: Optional[str] = None
    quoted_total: Optional[float] = None


class EventOut(EventBase):
    id: int
    payments_total: float
    expenses_total: float
    labor_total: float
    outstanding_amount: float
    payment_status: str
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


# ----------------------
# Expense Schemas
# ----------------------
class ExpenseBase(BaseModel):
    event_id: Optional[int] = None
    amount: float
    category: Optional[str] = None
    description: Optional[str] = None
    expense_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    event_id: Optional[int] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True


# ----------------------
# Event Extras Schemas
# ----------------------
class EventServiceCreate(BaseModel):
    name: str
    quantity: int
    unit_price: float


class EventContactCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    note: Optional[str] = None


class EventAssignmentCreate(BaseModel):
    employee_id: Optional[int] = None
    role: Optional[str] = None
    hours: float
    hourly_rate: float