from sqlalchemy import String, ForeignKey, Column, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin

class Category(AuditMixin, Base):
    __tablename__ = "categories"
    name = Column(String(100))
    image_path = Column(String(255))
    description = Column(Text)
    parent_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    products = relationship("Product", back_populates="category")

