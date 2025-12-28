from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
from app.models.mixins import AuditMixin

class Voucher(AuditMixin, Base):
    __tablename__ = "vouchers"
    code = Column(String(50), unique=True, nullable=False)
    discount = Column(Float, nullable=False)
    description = Column(String(255))
    quantity = Column(Integer, nullable=False)
    min_order_amount = Column(Float, nullable=True)
    max_discount = Column(Float, nullable=True)
    limit = Column(Integer, nullable=True)