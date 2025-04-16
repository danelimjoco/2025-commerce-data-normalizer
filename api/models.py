# Pydantic models for request/response validation
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Base model with common product fields
class ProductBase(BaseModel):
    platform: str
    platform_id: str
    title: str
    price: float
    currency: str
    quantity: int
    created_at: datetime

# Full product model including database-specific fields
class Product(ProductBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility

# Response model for list endpoints
class ProductResponse(BaseModel):
    data: List[Product]  # List of products
    meta: dict  # Pagination metadata

# Pagination parameters
class PaginationParams(BaseModel):
    page: int = 1  # Current page number
    per_page: int = 20  # Items per page

# Available filters for product queries
class ProductFilters(BaseModel):
    platform: Optional[str] = None  # Filter by platform
    min_price: Optional[float] = None  # Minimum price
    max_price: Optional[float] = None  # Maximum price
    min_quantity: Optional[int] = None  # Minimum quantity
    search: Optional[str] = None  # Search in product titles 