import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import declarative_mixin


def generate_uuid_str() -> str:
    return str(uuid.uuid4())


@declarative_mixin
class AuditMixin:
    id = Column(String(36), primary_key=True, default=generate_uuid_str)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    deleted_by = Column(String(36), nullable=True)
