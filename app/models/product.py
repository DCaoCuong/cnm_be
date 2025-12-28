from sqlalchemy import String, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Product(AuditMixin, Base):
    __tablename__ = "products"
    name = Column(String(200))
    brand_id = Column(String(36), ForeignKey("brands.id"))
    category_id = Column(String(36), ForeignKey("categories.id"))
    description = Column(String(255))
    thumbnail = Column(String(255))
    is_active = Column(Boolean, default=True)

    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    product_types = relationship("ProductType", back_populates="product")
