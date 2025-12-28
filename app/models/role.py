from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Role(AuditMixin, Base):
    __tablename__ = "roles"
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable = True)
    # relationship to users via user_roles junction table
    users = relationship("User", secondary="user_roles", back_populates="roles")
