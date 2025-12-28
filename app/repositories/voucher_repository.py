from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, asc, desc
from app.models.voucher import Voucher
from app.repositories.base import BaseRepository


class VoucherRepository(BaseRepository[Voucher]):
    """Repository cho Voucher model"""
    
    def __init__(self, db: Session):
        super().__init__(Voucher, db)
    
    def get_by_code(self, code: str) -> Optional[Voucher]:
        """Lấy voucher theo code (không bao gồm deleted)"""
        return self.db.query(Voucher).filter(
            and_(
                Voucher.code == code,
                Voucher.deleted_at.is_(None)
            )
        ).first()
    
    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        q: Optional[str] = None,
        min_discount: Optional[float] = None,
        max_discount: Optional[float] = None,
        sort_by: str = "id",
        sort_dir: str = "desc",
    ) -> Tuple[List[Voucher], int]:
        """Tìm kiếm vouchers với filter và sort"""
        query = self.db.query(Voucher).filter(Voucher.deleted_at.is_(None))
        
        # Search by code or description
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    Voucher.code.ilike(like),
                    Voucher.description.ilike(like)
                )
            )
        
        # Filter by discount range
        if min_discount is not None:
            query = query.filter(Voucher.discount >= min_discount)
        if max_discount is not None:
            query = query.filter(Voucher.discount <= max_discount)
        
        # Count total
        total = query.count()
        
        # Sorting
        sort_col = getattr(Voucher, sort_by, None)
        if sort_col is None:
            sort_col = Voucher.id
        
        if sort_dir and sort_dir.lower() == "asc":
            query = query.order_by(asc(sort_col))
        else:
            query = query.order_by(desc(sort_col))
        
        # Pagination
        items = query.offset(skip).limit(limit).all()
        return items, total

