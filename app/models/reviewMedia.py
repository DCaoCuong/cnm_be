from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import AuditMixin


class ReviewMedia(AuditMixin, Base):
    __tablename__ = "review_medias"
    review_id = Column(String(36), ForeignKey("reviews.id"))
    path = Column(String(255))
    review = relationship("Review", back_populates="medias")

