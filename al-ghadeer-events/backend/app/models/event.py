from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_date_status", "date", "status"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=True)
    organizer = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True, default="scheduled", index=True)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = relationship("Task", back_populates="event")
    payments = relationship("Payment", back_populates="event")