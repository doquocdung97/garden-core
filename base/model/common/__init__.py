from sqlalchemy import create_engine, Column, Integer, String,DateTime
from datetime import datetime
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
