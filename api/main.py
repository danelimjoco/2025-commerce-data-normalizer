from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas, models
from .database import get_db
from .utils.pagination import paginate
from .utils.filters import apply_filters

app = FastAPI(
    title="E-commerce API",
    description="API for accessing normalized e-commerce product data",
    version="1.0.0"
)

@app.get("/api/products", response_model=models.ProductResponse)
async def get_products(
    page: int = 1,
    per_page: int = 20,
    platform: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering and pagination."""
    filters = models.ProductFilters(
        platform=platform,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        search=search
    )
    
    query = db.query(schemas.Product)
    query = apply_filters(query, filters)
    paginated_query, total = paginate(query, page, per_page)
    
    products = paginated_query.all()
    
    return {
        "data": products,
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total
        }
    }

@app.get("/api/products/{product_id}", response_model=models.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID."""
    product = db.query(schemas.Product).filter(schemas.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/products/platform/{platform}", response_model=models.ProductResponse)
async def get_products_by_platform(
    platform: str,
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db)
):
    """Get all products from a specific platform."""
    query = db.query(schemas.Product).filter(schemas.Product.platform == platform)
    paginated_query, total = paginate(query, page, per_page)
    
    products = paginated_query.all()
    
    return {
        "data": products,
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 