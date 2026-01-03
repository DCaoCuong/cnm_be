from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.product import Product
from app.models.productType import ProductType  
from app.models.review import Review
from app.models.wishlist import Wishlist
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository cho Product với các method truy vấn sản phẩm"""

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_detail(self, product_id: str) -> Optional[Product]:
        """Lấy chi tiết sản phẩm theo ID"""
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.deleted_at.is_(None),
            Product.is_active == True
        ).first()

    def get_by_brand(self, brand_id: str, limit: int = 20, skip: int = 0) -> List[Product]:
        """Lấy danh sách sản phẩm theo brand"""
        return self.db.query(Product).filter(
            Product.brand_id == brand_id,
            Product.deleted_at.is_(None),
            Product.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_category(self, category_id: str, limit: int = 20, skip: int = 0) -> List[Product]:
        """Lấy danh sách sản phẩm theo category"""
        return self.db.query(Product).filter(
            Product.category_id == category_id,
            Product.deleted_at.is_(None),
            Product.is_active == True
        ).offset(skip).limit(limit).all()

    def get_best_selling(self, limit: int = 10) -> List[Tuple[Product, int]]:
        """Lấy top sản phẩm bán chạy nhất (dựa vào số lượng đã bán của product_types)"""
        return self.db.query(Product, func.sum(ProductType.sold).label('total_sold')).join(
            ProductType, Product.id == ProductType.product_id
        ).filter(
            Product.deleted_at.is_(None),
            Product.is_active == True
        ).group_by(Product.id).order_by(
            desc('total_sold')
        ).limit(limit).all()

    def get_most_favorite(self, limit: int = 10) -> List[Tuple[Product, int]]:
        """Lấy top sản phẩm được yêu thích nhất (dựa vào số lượng trong wishlist)"""
        return self.db.query(Product, func.count(Wishlist.id).label('favorite_count')).join(
            Wishlist, Product.id == Wishlist.product_id
        ).filter(
            Product.deleted_at.is_(None),
            Product.is_active == True
        ).group_by(Product.id).order_by(
            desc('favorite_count')
        ).limit(limit).all()