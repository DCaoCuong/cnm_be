from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.brand import Brand
from app.repositories.brand_repository import BrandRepository
from app.schemas.request.brand import BrandCreate, BrandUpdate


def get_brand(db: Session, brand_id: str) -> Optional[Brand]:
    repo = BrandRepository(db)
    return repo.get(brand_id)


def get_brand_by_name(db: Session, name: str) -> Optional[Brand]:
    repo = BrandRepository(db)
    return repo.get_by_name(name)


def get_brands(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    sort_by: str = "id",
    sort_dir: str = "desc",
) -> Tuple[List[Brand], int]:
    repo = BrandRepository(db)
    return repo.search(
        skip=skip,
        limit=limit,
        q=q,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


def create_brand(db: Session, brand_in: BrandCreate, created_by: Optional[str] = None) -> Brand:
    repo = BrandRepository(db)
    return repo.create(brand_in.dict(), created_by=created_by)


def update_brand(db: Session, brand_id: str, brand_in: BrandUpdate, updated_by: Optional[str] = None) -> Optional[Brand]:
    repo = BrandRepository(db)
    update_data = brand_in.dict(exclude_unset=True)
    return repo.update(brand_id, update_data, updated_by=updated_by)


def soft_delete_brand(db: Session, brand_id: str, deleted_by: Optional[str] = None) -> bool:
    repo = BrandRepository(db)
    return repo.delete(brand_id, deleted_by=deleted_by)
