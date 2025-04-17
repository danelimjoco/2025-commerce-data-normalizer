# Pydantic models for request/response validation
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MerchantMetricsBase(BaseModel):
    platform: str
    merchant_name: str
    total_sales: float
    total_orders: int
    average_order_value: float
    total_customers: int
    total_products: int

class MerchantMetricsCreate(MerchantMetricsBase):
    pass

class MerchantMetrics(MerchantMetricsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MerchantMetricsResponse(BaseModel):
    data: list[MerchantMetrics]
    meta: dict 