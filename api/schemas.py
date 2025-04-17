# SQLAlchemy model for merchant metrics
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base
from pydantic import BaseModel
from typing import List

# Database model for storing merchant metrics per platform
class MerchantPlatformMetrics(Base):
    __tablename__ = "merchant_metrics"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String(10), nullable=False)
    platform = Column(String(50), nullable=False)
    merchant_name = Column(String(255), nullable=False)
    total_sales = Column(Float, nullable=False)
    total_orders = Column(Integer, nullable=False)
    average_order_value = Column(Float, nullable=False)
    total_customers = Column(Integer, nullable=False)
    total_products = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        # Ensure a merchant can only have one record per platform
        {'sqlite_autoincrement': True},
    )

# Response models for the API
class PlatformStats(BaseModel):
    platform: str
    total_merchants: int
    total_sales: float
    total_orders: int
    average_order_value: float
    total_customers: int
    total_products: int

class MerchantPlatformStats(BaseModel):
    platform: str
    total_sales: float
    total_orders: int
    average_order_value: float
    total_customers: int
    total_products: int
    updated_at: datetime

class MerchantMetrics(BaseModel):
    merchant_id: str
    merchant_name: str
    platforms: List[MerchantPlatformStats]
    total_sales: float
    total_orders: int
    average_order_value: float
    total_customers: int 