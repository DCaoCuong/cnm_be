from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.voucher import Voucher
from app.repositories.voucher_repository import VoucherRepository
from app.schemas.request.voucher import VoucherCreate, VoucherUpdate


def get_voucher(db: Session, voucher_id: str) -> Optional[Voucher]:
    """Lấy voucher theo ID (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    return voucher_repo.get(voucher_id)


def get_voucher_by_code(db: Session, code: str) -> Optional[Voucher]:
    """Lấy voucher theo code (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    return voucher_repo.get_by_code(code)


def get_vouchers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    min_discount: Optional[float] = None,
    max_discount: Optional[float] = None,
    sort_by: str = "id",
    sort_dir: str = "desc",
) -> Tuple[List[Voucher], int]:
    """Lấy danh sách vouchers với search, filter và sort (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    return voucher_repo.search(
        skip=skip,
        limit=limit,
        q=q,
        min_discount=min_discount,
        max_discount=max_discount,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


def create_voucher(db: Session, voucher_in: VoucherCreate, created_by: Optional[str] = None) -> Voucher:
    """Tạo voucher mới (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    return voucher_repo.create(voucher_in.dict(), created_by=created_by)


def update_voucher(db: Session, voucher_id: str, voucher_in: VoucherUpdate, updated_by: Optional[str] = None) -> Optional[Voucher]:
    """Cập nhật voucher (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    update_data = voucher_in.dict(exclude_unset=True)
    return voucher_repo.update(voucher_id, update_data, updated_by=updated_by)


def soft_delete_voucher(db: Session, voucher_id: str, deleted_by: Optional[str] = None) -> bool:
    """Soft delete voucher (sử dụng repository)"""
    voucher_repo = VoucherRepository(db)
    return voucher_repo.delete(voucher_id, deleted_by=deleted_by)