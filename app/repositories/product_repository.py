from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from app.models.product import Product
from app.models.orderDetail import OrderDetail
from app.models.review import Review
from app.repositories.base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_detail(self, id: str):
        return self.db.query(Product)\
            .options(
                joinedload(Product.brand),
                joinedload(Product.category),
                joinedload(Product.product_types)
            )\
            .filter(Product.id == id, Product.deleted_at.is_(None))\
            .first()

    def get_by_brand(self, brand_id: str, limit: int = 20, skip: int = 0):
        return self.db.query(Product).filter(
            Product.brand_id == brand_id,
            Product.deleted_at.is_(None),
            Product.is_active == True,
        ).options(joinedload(Product.product_types)).offset(skip).limit(limit).all()

    def get_by_category(self, category_id: str, limit: int = 20, skip: int = 0):
        return self.db.query(Product).filter(
            Product.category_id == category_id,
            Product.deleted_at.is_(None),
            Product.is_active == True,
        ).options(joinedload(Product.product_types)).offset(skip).limit(limit).all()

    def get_best_selling(self, limit: int = 10):
        return self.db.query(
                Product,
                func.sum(OrderDetail.quantity).label("total_sold")
            )\
            .join(OrderDetail, OrderDetail.product_id == Product.id)\
            .filter(Product.deleted_at.is_(None), Product.is_active == True)\
            .group_by(Product.id)\
            .order_by(desc("total_sold"))\
            .limit(limit)\
            .all()

    def get_most_favorite(self, limit: int = 10):
        return self.db.query(
                Product,
                func.avg(Review.rating).label("avg_rating")
            )\
            .join(Review, Review.product_id == Product.id)\
            .filter(Product.deleted_at.is_(None), Product.is_active == True)\
            .group_by(Product.id)\
            .order_by(desc("avg_rating"))\
            .limit(limit)\
            .all()