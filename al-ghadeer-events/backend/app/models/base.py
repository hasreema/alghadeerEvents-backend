from datetime import datetime
from sqlalchemy import Column, Integer, DateTime


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class IdMixin:
    id = Column(Integer, primary_key=True, index=True)