# SQLAlchemy model for the products table
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    # Define the table name and schema
    __tablename__ = "products"
    __table_args__ = (
        {'schema': 'public'},
    )

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Platform information
    platform = Column(String(50), nullable=False)  # e.g., 'shopify', 'woocommerce'
    platform_id = Column(String(255), nullable=False)  # Original ID from the platform
    
    # Product details
    title = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)  # e.g., 'USD', 'EUR'
    quantity = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, 
                       server_default=func.now(),  # Default to current time
                       onupdate=func.now())  # Update on change 