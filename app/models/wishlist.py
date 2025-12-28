from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class Wishlist(AuditMixin, Base):
    __tablename__ = "wishlists"
    user_id = Column(String(36), ForeignKey("users.id"))
    items = relationship("WishlistItem", back_populates="wishlist")

