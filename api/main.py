# FastAPI application for the e-commerce API
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from . import models, schemas
from .utils.pagination import paginate

# Create FastAPI application with metadata
app = FastAPI(
    title="E-commerce API",
    description="API for managing merchant metrics across different e-commerce platforms",
    version="1.0.0"
)

@app.get("/merchant-metrics/", response_model=List[schemas.MerchantMetrics])
async def get_merchant_metrics(
    platform: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    """Get all merchant metrics with optional filtering and pagination"""
    query = db.query(models.MerchantMetrics)
    if platform:
        query = query.filter(models.MerchantMetrics.platform == platform)
    return paginate(query, page, per_page)

@app.get("/merchant-metrics/{merchant_id}", response_model=schemas.MerchantMetrics)
async def get_merchant_metric(merchant_id: int, db: Session = Depends(get_db)):
    """Get a single merchant's metrics by ID"""
    merchant = db.query(models.MerchantMetrics).filter(models.MerchantMetrics.id == merchant_id).first()
    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 