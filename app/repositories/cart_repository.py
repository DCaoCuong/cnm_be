from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[Cart]):
    def __init__(self, db: Session):
        super().__init__(Cart, db)

    def get_by_user(self, user_id: str) -> Optional[Cart]:
        return self.db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.deleted_at.is_(None),
        ).first()


class CartItemRepository(BaseRepository[CartItem]):
    def __init__(self, db: Session):
        super().__init__(CartItem, db)

    def list_by_cart(self, cart_id: str, skip: int = 0, limit: int = 100) -> Tuple[List[CartItem], int]:
        query = self.db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.deleted_at.is_(None),
        )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
