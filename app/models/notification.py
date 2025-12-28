from sqlalchemy import Column, String, DateTime, Boolean, Text
from app.core.database import Base
from app.models.mixins import AuditMixin


class Notification(AuditMixin, Base):
    __tablename__ = "notifications"
    title = Column(String(200))
    content = Column(Boolean)
    type = Column(String(50))
    sender_id = Column(String(36))
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
