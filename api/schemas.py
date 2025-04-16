from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    platform_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        {'schema': 'public'},
    ) 