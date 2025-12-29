from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WishlistItemBase(BaseModel):
    product_type_id: str = Field(...)


class WishlistItemCreate(WishlistItemBase):
    pass


class WishlistItemInDBBase(WishlistItemBase):
    id: str
    wishlist_id: str
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class WishlistItemResponse(WishlistItemInDBBase):
    pass


class WishlistBase(BaseModel):
    pass


class WishlistCreate(WishlistBase):
    pass


class WishlistInDBBase(WishlistBase):
    id: str
    user_id: str
    items: Optional[List[WishlistItemResponse]] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class WishlistResponse(WishlistInDBBase):
    pass
