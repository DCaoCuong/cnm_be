from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.request.wishlist import (
    WishlistResponse,
    WishlistItemCreate,
    WishlistItemResponse,
)
from app.schemas.response.base import BaseResponse
from app.services.wishlist_service import (
    create_wishlist_for_user,
    get_wishlist_by_user,
    add_wishlist_item,
    list_wishlist_items,
    remove_wishlist_item,
    get_wishlist_item,
)

router = APIRouter(prefix="/wishlists", tags=["wishlists"])


@router.post("/", response_model=BaseResponse[WishlistResponse], status_code=status.HTTP_201_CREATED)
def create_wishlist(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    obj = create_wishlist_for_user(db, str(current_user.id), created_by=str(current_user.id))
    return BaseResponse(success=True, message="Created", data=obj)


@router.get("/me", response_model=BaseResponse[WishlistResponse])
def get_my_wishlist(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    obj = get_wishlist_by_user(db, str(current_user.id))
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found")
    return BaseResponse(success=True, message="OK", data=obj)


@router.post("/{wishlist_id}/items", response_model=BaseResponse[WishlistItemResponse], status_code=status.HTTP_201_CREATED)
def add_item(wishlist_id: str, item_in: WishlistItemCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    obj = add_wishlist_item(db, wishlist_id, item_in, created_by=str(current_user.id))
    return BaseResponse(success=True, message="Created", data=obj)


@router.get("/{wishlist_id}/items", response_model=BaseResponse[List[WishlistItemResponse]])
def list_items(wishlist_id: str, db: Session = Depends(get_db)):
    items, total = list_wishlist_items(db, wishlist_id)
    meta = {"total": total}
    return BaseResponse(success=True, message="OK", data=items, meta=meta)


@router.delete("/{wishlist_id}/items/{item_id}", response_model=BaseResponse[None])
def delete_item(wishlist_id: str, item_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    obj = get_wishlist_item(db, item_id)
    if not obj or obj.wishlist_id != wishlist_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    ok = remove_wishlist_item(db, item_id, deleted_by=str(current_user.id))
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return BaseResponse(success=True, message="Deleted", data=None)
