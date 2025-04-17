# FastAPI application for the e-commerce API
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas
from .database import SessionLocal, engine
from datetime import datetime

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/merchants/{merchant_id}/metrics", response_model=schemas.MerchantMetrics)
async def get_merchant_metrics(
    merchant_id: str,
    platform: Optional[str] = Query(None, description="Filter by platform (shopify or woocommerce)"),
    db: Session = Depends(get_db)
):
    """
    Get metrics for a merchant across all platforms.
    Optionally filter by a specific platform.
    """
    query = db.query(schemas.MerchantPlatformMetrics).filter(
        schemas.MerchantPlatformMetrics.merchant_id == merchant_id
    )
    
    if platform:
        if platform not in ['shopify', 'woocommerce']:
            raise HTTPException(status_code=400, detail="Invalid platform. Must be 'shopify' or 'woocommerce'")
        query = query.filter(schemas.MerchantPlatformMetrics.platform == platform)
    
    metrics = query.all()
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # Calculate aggregated totals
    total_sales = sum(m.total_sales for m in metrics)
    total_orders = sum(m.total_orders for m in metrics)
    total_customers = sum(m.total_customers for m in metrics)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    # Convert database models to response models
    platform_stats = [
        schemas.MerchantPlatformStats(
            platform=m.platform,
            total_sales=m.total_sales,
            total_orders=m.total_orders,
            average_order_value=m.average_order_value,
            total_customers=m.total_customers,
            total_products=m.total_products,
            updated_at=m.updated_at
        ) for m in metrics
    ]
    
    return schemas.MerchantMetrics(
        merchant_id=merchant_id,
        merchant_name=metrics[0].merchant_name,
        platforms=platform_stats,
        total_sales=total_sales,
        total_orders=total_orders,
        average_order_value=avg_order_value,
        total_customers=total_customers
    )

@app.get("/platforms/{platform}/stats", response_model=schemas.PlatformStats)
async def get_platform_stats(platform: str, db: Session = Depends(get_db)):
    """
    Get aggregated statistics for a specific platform.
    """
    if platform not in ['shopify', 'woocommerce']:
        raise HTTPException(status_code=400, detail="Invalid platform. Must be 'shopify' or 'woocommerce'")
    
    merchants = db.query(schemas.MerchantPlatformMetrics).filter(schemas.MerchantPlatformMetrics.platform == platform).all()
    
    if not merchants:
        return schemas.PlatformStats(
            platform=platform,
            total_merchants=0,
            total_sales=0,
            total_orders=0,
            average_order_value=0,
            total_customers=0,
            total_products=0
        )
    
    total_sales = sum(m.total_sales for m in merchants)
    total_orders = sum(m.total_orders for m in merchants)
    total_customers = sum(m.total_customers for m in merchants)
    total_products = sum(m.total_products for m in merchants)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return schemas.PlatformStats(
        platform=platform,
        total_merchants=len(merchants),
        total_sales=total_sales,
        total_orders=total_orders,
        average_order_value=avg_order_value,
        total_customers=total_customers,
        total_products=total_products
    )

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