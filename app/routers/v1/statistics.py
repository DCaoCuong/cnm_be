"""
Statistics Router - API thống kê cho Admin
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.dependencies.database import get_db
from app.dependencies.permission import require_roles
from app.schemas.response.base import BaseResponse
from app.models.product import Product
from app.models.productType import ProductType
from app.models.order import Order
from app.models.orderDetail import OrderDetail

router = APIRouter()


class TopFilter(int, Enum):
    top_5 = 5
    top_10 = 10
    top_15 = 15
    top_20 = 20


class BestSellingProductResponse(BaseModel):
    """Response cho sản phẩm bán chạy"""
    id: str
    name: str
    thumbnail: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    total_sold: int
    total_revenue: float

    class Config:
        from_attributes = True


class ProductStatisticsResponse(BaseModel):
    """Response cho thống kê sản phẩm"""
    total_products: int
    total_active_products: int
    total_sold_items: int
    total_revenue: float
    best_selling: List[BestSellingProductResponse]


@router.get("/products/best-selling", response_model=BaseResponse[List[BestSellingProductResponse]])
def get_best_selling_statistics(
    top: TopFilter = Query(TopFilter.top_10, description="Số lượng top sản phẩm: 5, 10, 15, 20"),
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    """
    Thống kê sản phẩm bán chạy nhất (Admin only)
    
    - **top**: Số lượng top sản phẩm (5, 10, 15, 20)
    
    Returns danh sách sản phẩm với:
    - total_sold: Tổng số lượng đã bán
    - total_revenue: Tổng doanh thu
    """
    # Query sản phẩm bán chạy với doanh thu
    results = db.query(
        Product.id,
        Product.name,
        Product.thumbnail,
        Product.category_id,
        Product.brand_id,
        func.coalesce(func.sum(ProductType.sold), 0).label('total_sold'),
        func.coalesce(
            func.sum(ProductType.sold * func.coalesce(ProductType.discount_price, ProductType.price)),
            0
        ).label('total_revenue')
    ).outerjoin(
        ProductType, Product.id == ProductType.product_id
    ).filter(
        Product.deleted_at.is_(None),
        Product.is_active == True
    ).group_by(
        Product.id
    ).order_by(
        desc('total_sold')
    ).limit(top.value).all()
    
    # Convert to response
    data = [
        BestSellingProductResponse(
            id=r.id,
            name=r.name,
            thumbnail=r.thumbnail,
            category_id=r.category_id,
            brand_id=r.brand_id,
            total_sold=int(r.total_sold or 0),
            total_revenue=float(r.total_revenue or 0)
        )
        for r in results
    ]
    
    return BaseResponse(
        success=True,
        message=f"Lấy top {top.value} sản phẩm bán chạy thành công.",
        data=data
    )


@router.get("/products/summary", response_model=BaseResponse[ProductStatisticsResponse])
def get_product_statistics_summary(
    top: TopFilter = Query(TopFilter.top_5, description="Số lượng top sản phẩm"),
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    """
    Thống kê tổng quan sản phẩm (Admin only)
    
    Returns:
    - total_products: Tổng số sản phẩm
    - total_active_products: Số sản phẩm đang hoạt động  
    - total_sold_items: Tổng số lượng đã bán
    - total_revenue: Tổng doanh thu
    - best_selling: Top sản phẩm bán chạy
    """
    # Tổng sản phẩm
    total_products = db.query(func.count(Product.id)).filter(
        Product.deleted_at.is_(None)
    ).scalar() or 0
    
    # Sản phẩm active
    total_active = db.query(func.count(Product.id)).filter(
        Product.deleted_at.is_(None),
        Product.is_active == True
    ).scalar() or 0
    
    # Tổng số lượng đã bán
    total_sold = db.query(func.coalesce(func.sum(ProductType.sold), 0)).scalar() or 0
    
    # Tổng doanh thu
    total_revenue = db.query(
        func.coalesce(
            func.sum(ProductType.sold * func.coalesce(ProductType.discount_price, ProductType.price)),
            0
        )
    ).scalar() or 0
    
    # Best selling
    best_selling_results = db.query(
        Product.id,
        Product.name,
        Product.thumbnail,
        Product.category_id,
        Product.brand_id,
        func.coalesce(func.sum(ProductType.sold), 0).label('total_sold'),
        func.coalesce(
            func.sum(ProductType.sold * func.coalesce(ProductType.discount_price, ProductType.price)),
            0
        ).label('total_revenue')
    ).outerjoin(
        ProductType, Product.id == ProductType.product_id
    ).filter(
        Product.deleted_at.is_(None),
        Product.is_active == True
    ).group_by(
        Product.id
    ).order_by(
        desc('total_sold')
    ).limit(top.value).all()
    
    best_selling = [
        BestSellingProductResponse(
            id=r.id,
            name=r.name,
            thumbnail=r.thumbnail,
            category_id=r.category_id,
            brand_id=r.brand_id,
            total_sold=int(r.total_sold or 0),
            total_revenue=float(r.total_revenue or 0)
        )
        for r in best_selling_results
    ]
    
    return BaseResponse(
        success=True,
        message="Lấy thống kê sản phẩm thành công.",
        data=ProductStatisticsResponse(
            total_products=total_products,
            total_active_products=total_active,
            total_sold_items=int(total_sold),
            total_revenue=float(total_revenue),
            best_selling=best_selling
        )
    )



class DailyRevenueResponse(BaseModel):
    """Response cho doanh thu theo ngày"""
    date: str
    revenue: float
    orders_count: int


class DashboardStatsResponse(BaseModel):
    """Response cho dashboard statistics"""
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    daily_revenue: List[DailyRevenueResponse]


@router.get("/dashboard", response_model=BaseResponse[DashboardStatsResponse])
def get_dashboard_statistics(
    days: int = Query(7, ge=1, le=30, description="Số ngày thống kê doanh thu"),
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    """
    Thống kê tổng quan cho Dashboard (Admin only)
    
    Returns:
    - total_revenue: Tổng doanh thu từ đơn hàng completed
    - total_orders: Tổng số đơn hàng
    - total_customers: Tổng số khách hàng
    - total_products: Tổng số sản phẩm
    - daily_revenue: Doanh thu theo ngày (7 ngày gần nhất)
    """
    from app.models.user import User
    
    # Tổng doanh thu từ đơn hàng completed
    total_revenue = db.query(
        func.coalesce(func.sum(Order.total_amount), 0)
    ).filter(
        Order.status == 'completed',
        Order.deleted_at.is_(None)
    ).scalar() or 0
    
    # Tổng số đơn hàng
    total_orders = db.query(func.count(Order.id)).filter(
        Order.deleted_at.is_(None)
    ).scalar() or 0
    
    # Tổng số khách hàng (users không phải admin)
    total_customers = db.query(func.count(User.id)).filter(
        User.deleted_at.is_(None)
    ).scalar() or 0
    
    # Tổng số sản phẩm
    total_products = db.query(func.count(Product.id)).filter(
        Product.deleted_at.is_(None)
    ).scalar() or 0
    
    # Doanh thu theo ngày (X ngày gần nhất)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    daily_stats = db.query(
        func.date(Order.created_at).label('date'),
        func.coalesce(func.sum(Order.total_amount), 0).label('revenue'),
        func.count(Order.id).label('orders_count')
    ).filter(
        Order.status == 'completed',
        Order.deleted_at.is_(None),
        func.date(Order.created_at) >= start_date,
        func.date(Order.created_at) <= end_date
    ).group_by(
        func.date(Order.created_at)
    ).order_by(
        func.date(Order.created_at)
    ).all()
    
    # Tạo dict để fill missing dates
    daily_dict = {str(stat.date): stat for stat in daily_stats}
    
    # Fill missing dates with 0
    daily_revenue = []
    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)
        if date_str in daily_dict:
            stat = daily_dict[date_str]
            daily_revenue.append(DailyRevenueResponse(
                date=date_str,
                revenue=float(stat.revenue or 0),
                orders_count=int(stat.orders_count or 0)
            ))
        else:
            daily_revenue.append(DailyRevenueResponse(
                date=date_str,
                revenue=0.0,
                orders_count=0
            ))
        current_date += timedelta(days=1)
    
    return BaseResponse(
        success=True,
        message="Lấy thống kê dashboard thành công.",
        data=DashboardStatsResponse(
            total_revenue=float(total_revenue),
            total_orders=total_orders,
            total_customers=total_customers,
            total_products=total_products,
            daily_revenue=daily_revenue
        )
    )
