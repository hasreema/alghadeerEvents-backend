from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class EventService(Base):
    __tablename__ = "event_services"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    total_price = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event", back_populates="services")


class EventContact(Base):
    __tablename__ = "event_contacts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    note = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event", back_populates="contacts")


class EventAssignment(Base):
    __tablename__ = "event_assignments"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True, index=True)
    role = Column(String(100), nullable=True)
    hours = Column(Numeric(10, 2), nullable=False, default=0)
    hourly_rate = Column(Numeric(12, 2), nullable=False, default=0)
    total_cost = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event", back_populates="assignments")