# FastAPI application for the e-commerce API
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from .schemas import MerchantMetrics
from .models import MerchantMetrics as MerchantMetricsSchema
from .utils.pagination import paginate
from datetime import datetime

# Create FastAPI application with metadata
app = FastAPI(
    title="E-commerce API",
    description="API for managing merchant metrics across different e-commerce platforms",
    version="1.0.0"
)

@app.get("/merchant-metrics/", response_model=List[MerchantMetricsSchema])
async def get_merchant_metrics(
    platform: Optional[str] = Query(None, description="Filter by platform (shopify or woocommerce)"),
    min_sales: Optional[float] = Query(None, description="Minimum total sales amount"),
    max_sales: Optional[float] = Query(None, description="Maximum total sales amount"),
    min_orders: Optional[int] = Query(None, description="Minimum number of orders"),
    max_orders: Optional[int] = Query(None, description="Maximum number of orders"),
    page: int = Query(1, description="Page number for pagination"),
    per_page: int = Query(10, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all merchant metrics with filtering and pagination.
    
    - Filter by platform, sales range, and order count
    - Results are paginated
    - Returns detailed merchant metrics including sales, orders, and customer data
    """
    query = db.query(MerchantMetrics)
    
    if platform:
        query = query.filter(MerchantMetrics.platform == platform)
    if min_sales is not None:
        query = query.filter(MerchantMetrics.total_sales >= min_sales)
    if max_sales is not None:
        query = query.filter(MerchantMetrics.total_sales <= max_sales)
    if min_orders is not None:
        query = query.filter(MerchantMetrics.total_orders >= min_orders)
    if max_orders is not None:
        query = query.filter(MerchantMetrics.total_orders <= max_orders)
    
    paginated_query, _ = paginate(query, page, per_page)
    return paginated_query.all()

@app.get("/merchant-metrics/{merchant_id}", response_model=MerchantMetricsSchema)
async def get_merchant_metric(
    merchant_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed metrics for a specific merchant.
    
    - Returns all metrics including sales, orders, and customer data
    - Includes creation and last update timestamps
    """
    merchant = db.query(MerchantMetrics).filter(MerchantMetrics.merchant_id == merchant_id).first()
    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant

@app.get("/merchant-metrics/platform/{platform}/stats", response_model=dict)
async def get_platform_stats(
    platform: str,
    db: Session = Depends(get_db)
):
    """
    Get aggregated statistics for a specific platform.
    
    - Returns total merchants, total sales, average order value, etc.
    - Platform must be either 'shopify' or 'woocommerce'
    """
    if platform not in ['shopify', 'woocommerce']:
        raise HTTPException(status_code=400, detail="Invalid platform. Must be 'shopify' or 'woocommerce'")
    
    merchants = db.query(MerchantMetrics).filter(MerchantMetrics.platform == platform).all()
    
    if not merchants:
        return {
            "platform": platform,
            "total_merchants": 0,
            "total_sales": 0,
            "total_orders": 0,
            "average_order_value": 0,
            "total_customers": 0,
            "total_products": 0
        }
    
    return {
        "platform": platform,
        "total_merchants": len(merchants),
        "total_sales": sum(m.total_sales for m in merchants),
        "total_orders": sum(m.total_orders for m in merchants),
        "average_order_value": sum(m.average_order_value for m in merchants) / len(merchants),
        "total_customers": sum(m.total_customers for m in merchants),
        "total_products": sum(m.total_products for m in merchants)
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    - Returns API status and current timestamp
    - Useful for monitoring and uptime checks
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    } 