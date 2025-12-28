from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base
from app.models.mixins import AuditMixin


class UserNotification(AuditMixin, Base):
    __tablename__ = "user_notifications"
    user_id = Column(String(36), ForeignKey("users.id"))
    notification_id = Column(String(36), ForeignKey("notifications.id"))
