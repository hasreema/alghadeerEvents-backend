from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)
    organizer = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True, default="scheduled")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = relationship("Task", back_populates="event")