from sqlalchemy import String, ForeignKey, Column, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin

class Conversation(AuditMixin, Base):
    __tablename__ = "conversations"
    user1_id = Column(String(36), ForeignKey("users.id"))
    user2_id = Column(String(36), ForeignKey("users.id"))
    last_message = Column(Text)
    updated_at = Column(DateTime, onupdate=func.now())

