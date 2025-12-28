from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Payment(AuditMixin, Base):
    __tablename__ = "payments"
    order_id = Column(String(36), ForeignKey("orders.id"))
    method = Column(String(50))
    status = Column(String(50))
    order = relationship("Order", back_populates="payment")