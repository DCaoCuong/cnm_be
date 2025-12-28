from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base
from app.models.mixins import AuditMixin

class OrderVoucher(AuditMixin, Base):
    __tablename__ = "order_vouchers"
    order_id = Column(String(36), ForeignKey("orders.id"))
    voucher_id = Column(String(36), ForeignKey("vouchers.id"))