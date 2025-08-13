from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, Index

from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_employees_full_name", "full_name"),
        Index("ix_employees_role", "role"),
        Index("ix_employees_active", "is_active"),
    )

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=True)
    hourly_wage = Column(Numeric(12, 2), nullable=True)
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)