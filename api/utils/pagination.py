from sqlalchemy.orm import Query
from typing import Tuple

def paginate(query: Query, page: int, per_page: int) -> Tuple[Query, int]:
    """Apply pagination to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query to paginate
        page: Page number (1-based)
        per_page: Number of items per page
    
    Returns:
        Tuple of (paginated query, total count)
    """
    total = query.count()
    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page), total 