from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.models.wishlistItem import WishlistItem
from app.repositories.base import BaseRepository


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db: Session):
        super().__init__(Wishlist, db)

    def get_by_user(self, user_id: str) -> Optional[Wishlist]:
        return self.db.query(Wishlist).filter(
            Wishlist.user_id == user_id,
            Wishlist.deleted_at.is_(None),
        ).first()


class WishlistItemRepository(BaseRepository[WishlistItem]):
    def __init__(self, db: Session):
        super().__init__(WishlistItem, db)

    def list_by_wishlist(self, wishlist_id: str, skip: int = 0, limit: int = 100) -> Tuple[List[WishlistItem], int]:
        query = self.db.query(WishlistItem).filter(
            WishlistItem.wishlist_id == wishlist_id,
            WishlistItem.deleted_at.is_(None),
        )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
