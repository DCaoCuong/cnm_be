from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, EmailStr

class RoleResponse(BaseModel):
    id: Union[UUID, str]
    name: str
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: Union[UUID, str]  # Chấp nhận cả UUID và string
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool = True
    roles: List[RoleResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str     
    token_type: str = "bearer"
    scope: Optional[str] = ""
    expires_in: int
    refresh_expires_in: int 
    
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
