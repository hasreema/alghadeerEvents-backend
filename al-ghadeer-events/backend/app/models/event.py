from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_date_status", "date", "status"),
        Index("ix_events_title", "title"),
        Index("ix_events_location", "location"),
        Index("ix_events_payment_status", "payment_status"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # New enhanced fields
    name = Column(String(255), nullable=True, index=True)
    type = Column(String(50), nullable=True, index=True)
    type_custom = Column(String(100), nullable=True)
    starts_at = Column(DateTime, nullable=True, index=True)
    locations = Column(JSONB, nullable=True)  # array of strings
    gender = Column(String(20), nullable=True)
    guest_count = Column(Integer, nullable=True)
    special_requests = Column(JSONB, nullable=True)  # array of objects
    deposit_total = Column(Numeric(12, 2), nullable=True)
    deposit_paid = Column(Numeric(12, 2), nullable=True)
    phones = Column(JSONB, nullable=True)  # array of strings

    # Legacy / existing fields
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=True)
    organizer = Column(String(100), nullable=True)

    event_type = Column(String(50), nullable=True, index=True)
    status = Column(String(50), nullable=True, default="draft", index=True)

    # Financial fields
    quoted_total = Column(Numeric(12, 2), nullable=False, default=0)
    payments_total = Column(Numeric(12, 2), nullable=False, default=0)
    expenses_total = Column(Numeric(12, 2), nullable=False, default=0)
    labor_total = Column(Numeric(12, 2), nullable=False, default=0)
    outstanding_amount = Column(Numeric(12, 2), nullable=False, default=0)
    payment_status = Column(String(20), nullable=False, default="unpaid")

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = relationship("Task", back_populates="event")
    payments = relationship("Payment", back_populates="event")
    services = relationship("EventService", back_populates="event")
    contacts = relationship("EventContact", back_populates="event")
    assignments = relationship("EventAssignment", back_populates="event")