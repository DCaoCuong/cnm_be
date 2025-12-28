from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Order(AuditMixin, Base):
    __tablename__ = "orders"
    user_id = Column(String(36), ForeignKey("users.id"))
    status = Column(String(50))
    total_amount = Column(Float)
    discount_amount = Column(Float)
    final_amount = Column(Float)
    details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")