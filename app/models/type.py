from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin

class Type(AuditMixin, Base):
    __tablename__ = "types"
    name = Column(String(100))
    values = relationship("TypeValue", back_populates="type")

