# SQLAlchemy model for merchant metrics
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .database import Base

Base = declarative_base()

class MerchantMetrics(Base):
    __tablename__ = "merchant_metrics"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    merchant_name = Column(String(255), nullable=False)
    total_sales = Column(Float, nullable=False)
    total_orders = Column(Integer, nullable=False)
    average_order_value = Column(Float, nullable=False)
    total_customers = Column(Integer, nullable=False)
    total_products = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 