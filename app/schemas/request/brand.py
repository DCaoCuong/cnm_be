from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str = Field(..., max_length=100)
    image_path: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    image_path: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)


class BrandInDBBase(BrandBase):
    id: int
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class BrandResponse(BrandInDBBase):
    pass
