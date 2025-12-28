from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin

class WishlistItem(AuditMixin, Base):
    __tablename__ = "wishlist_items"
    wishlist_id = Column(String(36), ForeignKey("wishlists.id"))
    product_type_id = Column(String(36), ForeignKey("product_types.id"))
    wishlist = relationship("Wishlist", back_populates="items")
