# Repository layer for data access
from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.voucher_repository import VoucherRepository
from app.repositories.role_repository import RoleRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "VoucherRepository",
    "RoleRepository",
]

