from sqlalchemy.orm import Query
from ..models import ProductFilters
from ..schemas import Product

def apply_filters(query: Query, filters: ProductFilters) -> Query:
    """Apply filters to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query to filter
        filters: ProductFilters object containing filter criteria
    
    Returns:
        Filtered query
    """
    if filters.platform:
        query = query.filter(Product.platform == filters.platform)
    if filters.min_price is not None:
        query = query.filter(Product.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Product.price <= filters.max_price)
    if filters.min_quantity is not None:
        query = query.filter(Product.quantity >= filters.min_quantity)
    if filters.search:
        query = query.filter(Product.title.ilike(f"%{filters.search}%"))
    return query 