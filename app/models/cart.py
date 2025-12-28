from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Cart(AuditMixin, Base):
    __tablename__ = "carts"
    user_id = Column(String(36), ForeignKey("users.id"))
    items = relationship("CartItem", back_populates="cart")

