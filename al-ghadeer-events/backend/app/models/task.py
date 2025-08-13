from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_status_priority", "status", "priority"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    assigned_to = Column(String(100), nullable=True, index=True)
    due_date = Column(Date, nullable=True, index=True)
    status = Column(String(50), nullable=True, default="todo", index=True)
    priority = Column(String(50), nullable=True, default="normal", index=True)

    event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True, index=True)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event", back_populates="tasks")