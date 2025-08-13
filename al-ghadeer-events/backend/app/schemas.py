from datetime import date, time, datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field, validator


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
# Enhanced Event Schemas
# ----------------------
EventType = Literal['Wedding', 'Henna', 'Engagement', 'Graduation', 'Other']
GenderType = Literal['Men', 'Women', 'Mixed']
ProvidedBy = Literal['Hall', 'Client']
LocationPreset = Literal['Hall Floor 0', 'Hall Floor 1', 'Garden', 'Waterfall']


class SpecialRequest(BaseModel):
    name: str
    quantity: Optional[int] = None
    cost: float
    provided_by: ProvidedBy


class EventEnhancedCreate(BaseModel):
    name: str
    type: EventType
    type_custom: Optional[str] = None
    date: datetime
    locations: List[str]
    gender: GenderType
    guest_count: int
    description: Optional[str] = None
    special_requests: Optional[List[SpecialRequest]] = None
    deposit_total: float
    deposit_paid: float
    phones: List[str]

    @validator('type_custom')
    def validate_type_custom(cls, v, values):
        if values.get('type') == 'Other' and not v:
            raise ValueError("type_custom is required when type is 'Other'")
        return v

    @validator('locations')
    def validate_locations(cls, v):
        if not v or len(v) == 0:
            raise ValueError('locations must have at least one value')
        return v

    @validator('special_requests', each_item=True)
    def validate_special_requests(cls, v: SpecialRequest):
        if v.name.lower() == 'cake' and (v.quantity is None or v.quantity <= 0):
            raise ValueError('Cake requires quantity > 0')
        return v

    @validator('deposit_paid')
    def validate_deposit_paid(cls, v, values):
        total = values.get('deposit_total', 0)
        if v > total:
            raise ValueError('deposit_paid must be less than or equal to deposit_total')
        return v


class EventEnhancedUpdate(EventEnhancedCreate):
    pass


class EventEnhancedOut(EventEnhancedCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ----------------------
# Existing Event Schemas (kept)
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