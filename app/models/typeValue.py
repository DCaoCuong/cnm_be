from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin

class TypeValue(AuditMixin, Base):
    __tablename__ = "type_values"
    name = Column(String(100))
    type_id = Column(String(36), ForeignKey("types.id"))
    type = relationship("Type", back_populates="values")
