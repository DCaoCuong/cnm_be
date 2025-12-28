# Import Base từ core
from app.core.database import Base

# Import tất cả các model để SQLAlchemy đăng ký chúng vào Base.metadata
from app.models.mixins import AuditMixin
from app.models.address import Address
from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product
from app.models.type import Type
from app.models.typeValue import TypeValue
from app.models.productType import ProductType
from app.models.user import User
from app.models.role import Role
from app.models.userRole import UserRole
from app.models.voucher import Voucher
from app.models.order import Order
from app.models.orderDetail import OrderDetail
from app.models.orderVoucher import OrderVoucher
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.models.wishlist import Wishlist
from app.models.wishlistItem import WishlistItem
from app.models.review import Review
from app.models.reviewMedia import ReviewMedia
from app.models.notification import Notification
from app.models.userNotification import UserNotification
from app.models.conversation import Conversation
from app.models.message import Message

# Export Base để Alembic sử dụng
__all__ = ["Base"]