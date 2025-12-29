from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.models.wishlistItem import WishlistItem
from app.repositories.wishlist_repository import WishlistRepository, WishlistItemRepository
from app.schemas.request.wishlist import WishlistItemCreate


def get_wishlist_by_user(db: Session, user_id: str) -> Optional[Wishlist]:
    repo = WishlistRepository(db)
    return repo.get_by_user(user_id)


def create_wishlist_for_user(db: Session, user_id: str, created_by: Optional[str] = None) -> Wishlist:
    repo = WishlistRepository(db)
    existing = repo.get_by_user(user_id)
    if existing:
        return existing
    data = {"user_id": user_id}
    return repo.create(data, created_by=created_by)


def add_wishlist_item(db: Session, wishlist_id: str, item_in: WishlistItemCreate, created_by: Optional[str] = None) -> WishlistItem:
    repo = WishlistItemRepository(db)
    data = item_in.dict()
    data["wishlist_id"] = wishlist_id
    return repo.create(data, created_by=created_by)


def list_wishlist_items(db: Session, wishlist_id: str, skip: int = 0, limit: int = 100) -> Tuple[List[WishlistItem], int]:
    repo = WishlistItemRepository(db)
    return repo.list_by_wishlist(wishlist_id, skip=skip, limit=limit)


def remove_wishlist_item(db: Session, item_id: str, deleted_by: Optional[str] = None) -> bool:
    repo = WishlistItemRepository(db)
    return repo.delete(item_id, deleted_by=deleted_by)


def get_wishlist_item(db: Session, item_id: str) -> Optional[WishlistItem]:
    repo = WishlistItemRepository(db)
    return repo.get(item_id)
