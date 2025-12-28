from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class OrderDetail(AuditMixin, Base):
    __tablename__ = "order_details"
    order_id = Column(String(36), ForeignKey("orders.id"))
    product_type_id = Column(String(36), ForeignKey("product_types.id"))
    price = Column(Float)
    number = Column(Integer)
    order = relationship("Order", back_populates="details")