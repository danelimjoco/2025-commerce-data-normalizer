from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProductBase(BaseModel):
    platform: str
    platform_id: str
    title: str
    price: float
    currency: str
    quantity: int
    created_at: datetime

class Product(ProductBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    data: List[Product]
    meta: dict

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20

class ProductFilters(BaseModel):
    platform: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_quantity: Optional[int] = None
    search: Optional[str] = None 