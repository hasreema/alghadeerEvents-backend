from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        Index("ix_expenses_event_id", "event_id"),
        Index("ix_expenses_category", "category"),
        Index("ix_expenses_date", "expense_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True)

    amount = Column(Numeric(12, 2), nullable=False)
    category = Column(String(100), nullable=True)  # labor, decoration, food, misc
    description = Column(String(500), nullable=True)
    expense_date = Column(Date, nullable=False, default=datetime.utcnow)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event")