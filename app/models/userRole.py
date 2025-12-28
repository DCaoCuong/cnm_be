from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from app.core.database import Base
from app.models.mixins import AuditMixin

class UserRole(AuditMixin, Base):
    __tablename__ = "user_roles"

    # composite primary key (user_id, role_id)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    role_id = Column(String(36), ForeignKey("roles.id"), primary_key=True)

