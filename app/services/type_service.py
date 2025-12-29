from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.type import Type
from app.models.typeValue import TypeValue
from app.repositories.type_repository import TypeRepository
from app.repositories.type_value_repository import TypeValueRepository
from app.schemas.request.type import TypeCreate, TypeUpdate, TypeValueCreate, TypeValueUpdate


def get_type(db: Session, type_id: str) -> Optional[Type]:
    repo = TypeRepository(db)
    return repo.get(type_id)


def get_types(db: Session, skip: int = 0, limit: int = 100, q: Optional[str] = None, sort_by: str = "id", sort_dir: str = "desc") -> Tuple[List[Type], int]:
    repo = TypeRepository(db)
    return repo.search(skip=skip, limit=limit, q=q, sort_by=sort_by, sort_dir=sort_dir)


def create_type(db: Session, type_in: TypeCreate, created_by: Optional[str] = None) -> Type:
    repo = TypeRepository(db)
    return repo.create(type_in.dict(), created_by=created_by)


def update_type(db: Session, type_id: str, type_in: TypeUpdate, updated_by: Optional[str] = None) -> Optional[Type]:
    repo = TypeRepository(db)
    data = type_in.dict(exclude_unset=True)
    return repo.update(type_id, data, updated_by=updated_by)


def delete_type(db: Session, type_id: str, deleted_by: Optional[str] = None) -> bool:
    repo = TypeRepository(db)
    return repo.delete(type_id, deleted_by=deleted_by)


# TypeValue operations
def list_type_values(db: Session, type_id: str, skip: int = 0, limit: int = 100) -> Tuple[List[TypeValue], int]:
    repo = TypeValueRepository(db)
    return repo.list_by_type(type_id, skip=skip, limit=limit)


def get_type_value(db: Session, value_id: str) -> Optional[TypeValue]:
    repo = TypeValueRepository(db)
    return repo.get(value_id)


def create_type_value(db: Session, type_id: str, value_in: TypeValueCreate, created_by: Optional[str] = None) -> TypeValue:
    # ensure parent type exists
    type_repo = TypeRepository(db)
    if not type_repo.get(type_id):
        raise ValueError("Parent type not found")
    repo = TypeValueRepository(db)
    data = value_in.dict()
    data["type_id"] = type_id
    return repo.create(data, created_by=created_by)


def update_type_value(db: Session, value_id: str, value_in: TypeValueUpdate, updated_by: Optional[str] = None) -> Optional[TypeValue]:
    repo = TypeValueRepository(db)
    data = value_in.dict(exclude_unset=True)
    return repo.update(value_id, data, updated_by=updated_by)


def delete_type_value(db: Session, value_id: str, deleted_by: Optional[str] = None) -> bool:
    repo = TypeValueRepository(db)
    return repo.delete(value_id, deleted_by=deleted_by)
