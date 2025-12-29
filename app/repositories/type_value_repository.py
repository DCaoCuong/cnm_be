from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.typeValue import TypeValue
from app.repositories.base import BaseRepository


class TypeValueRepository(BaseRepository[TypeValue]):
    def __init__(self, db: Session):
        super().__init__(TypeValue, db)

    def get_by_name_and_type(self, name: str, type_id: str) -> Optional[TypeValue]:
        return self.db.query(TypeValue).filter(
            TypeValue.name == name,
            TypeValue.type_id == type_id,
            TypeValue.deleted_at.is_(None),
        ).first()

    def list_by_type(
        self,
        type_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[TypeValue], int]:
        query = self.db.query(TypeValue).filter(
            TypeValue.type_id == type_id,
            TypeValue.deleted_at.is_(None),
        )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
