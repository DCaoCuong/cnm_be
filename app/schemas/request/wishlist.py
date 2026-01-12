from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WishlistItemBase(BaseModel):
    product_type_id: str = Field(...)


class WishlistItemCreate(WishlistItemBase):
    pass


# Nested schemas for product info
class ProductMinimal(BaseModel):
    id: str
    name: str
    thumbnail: Optional[str] = None
    
    class Config:
        orm_mode = True


class ProductTypeMinimal(BaseModel):
    id: str
    product_id: str
    price: float
    discount_price: Optional[float] = None
    stock: int
    image_path: Optional[str] = None
    volume: Optional[str] = None
    skin_type: Optional[str] = None
    origin: Optional[str] = None
    is_available: bool = True
    product: Optional[ProductMinimal] = None
    
    class Config:
        orm_mode = True


class WishlistItemInDBBase(WishlistItemBase):
    id: str
    wishlist_id: str
    product_type: Optional[ProductTypeMinimal] = None
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
