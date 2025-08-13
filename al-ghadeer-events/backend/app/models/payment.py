from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payments_event_id", "event_id"),
        Index("ix_payments_status", "status"),
    )

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)

    amount = Column(Numeric(12, 2), nullable=False)
    method = Column(String(50), nullable=True)  # cash, card, transfer, check
    status = Column(String(50), nullable=True, default="paid")  # paid|pending|failed
    note = Column(String(500), nullable=True)
    receipt_url = Column(String(500), nullable=True)
    paid_at = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    event = relationship("Event", back_populates="payments")