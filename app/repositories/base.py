from typing import Generic, TypeVar, Optional, List, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository với các method CRUD cơ bản"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: str) -> Optional[ModelType]:
        """Lấy một record theo ID (không bao gồm deleted)"""
        return self.db.query(self.model).filter(
            and_(
                self.model.id == id,
                self.model.deleted_at.is_(None)
            )
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Lấy tất cả records (không bao gồm deleted)"""
        return self.db.query(self.model).filter(
            self.model.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def create(self, obj_data: dict, created_by: Optional[str] = None) -> ModelType:
        """Tạo mới một record"""
        obj = self.model(**obj_data)
        if created_by is not None and hasattr(obj, 'created_by'):
            obj.created_by = created_by
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, id: str, obj_data: dict, updated_by: Optional[str] = None) -> Optional[ModelType]:
        """Cập nhật một record"""
        obj = self.get(id)
        if not obj:
            return None
        
        for field, value in obj_data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        
        if updated_by is not None and hasattr(obj, 'updated_by'):
            obj.updated_by = updated_by
        
        if hasattr(obj, 'updated_at'):
            obj.updated_at = datetime.utcnow()
        
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: str, deleted_by: Optional[str] = None) -> bool:
        """Soft delete một record"""
        obj = self.get(id)
        if not obj:
            return False
        
        if hasattr(obj, 'deleted_at'):
            obj.deleted_at = datetime.utcnow()
        if deleted_by is not None and hasattr(obj, 'deleted_by'):
            obj.deleted_by = deleted_by
        
        self.db.add(obj)
        self.db.commit()
        return True
    
    def hard_delete(self, id: str) -> bool:
        """Hard delete một record (xóa vĩnh viễn)"""
        obj = self.get(id)
        if not obj:
            return False
        
        self.db.delete(obj)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Đếm số lượng records (không bao gồm deleted)"""
        return self.db.query(self.model).filter(
            self.model.deleted_at.is_(None)
        ).count()

