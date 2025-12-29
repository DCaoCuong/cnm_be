from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app.models.brand import Brand
from app.repositories.base import BaseRepository


class BrandRepository(BaseRepository[Brand]):
    def __init__(self, db: Session):
        super().__init__(Brand, db)

    def get_by_name(self, name: str) -> Optional[Brand]:
        return self.db.query(Brand).filter(
            Brand.name == name,
            Brand.deleted_at.is_(None),
        ).first()

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        q: Optional[str] = None,
        sort_by: str = "id",
        sort_dir: str = "desc",
    ) -> Tuple[List[Brand], int]:
        query = self.db.query(Brand).filter(Brand.deleted_at.is_(None))

        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    Brand.name.ilike(like),
                    Brand.description.ilike(like),
                )
            )

        total = query.count()

        sort_col = getattr(Brand, sort_by, None)
        if sort_col is None:
            sort_col = Brand.id

        if sort_dir and sort_dir.lower() == "asc":
            query = query.order_by(asc(sort_col))
        else:
            query = query.order_by(desc(sort_col))

        items = query.offset(skip).limit(limit).all()
        return items, total
