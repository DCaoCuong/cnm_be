from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository cho Role model"""
    
    def __init__(self, db: Session):
        super().__init__(Role, db)
    
    def get_by_name(self, name: str) -> Optional[Role]:
        """Lấy role theo tên (case-insensitive, không bao gồm deleted)"""
        return self.db.query(Role).filter(
            and_(
                Role.name.ilike(name),
                Role.deleted_at.is_(None)
            )
        ).first()
    
    def get_or_create(self, name: str, created_by: Optional[str] = None) -> Role:
        """Lấy role hoặc tạo mới nếu chưa tồn tại"""
        role = self.get_by_name(name)
        if not role:
            role = self.create(
                {"name": name.upper()},
                created_by=created_by
            )
        return role

