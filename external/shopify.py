from datetime import datetime, timedelta
import random
from .base import BaseAPI

class ShopifyAPI(BaseAPI):
    def __init__(self):
        super().__init__("shopify")
        self.mock_data = self._generate_mock_data()

    def _generate_mock_data(self):
        # Generate a unique timestamp-based prefix for this run
        timestamp = int(datetime.utcnow().timestamp())
        return [
            {
                "id": f"shopify_{timestamp}_{i}",  # Unique ID with timestamp
                "title": f"Shopify Product {i}",
                "price": random.uniform(10, 1000),
                "currency": "USD",
                "quantity": random.randint(0, 100),
                "updated_at": datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
            }
            for i in range(1000)
        ]

    async def get_products(self, page: int = 1, per_page: int = 50) -> dict:
        # Randomly select how many records to return (1-50)
        records_to_return = random.randint(1, 50)
        start = (page - 1) * per_page
        end = start + records_to_return
        products = self.mock_data[start:end]
        
        return {
            "data": products,
            "meta": {
                "current_page": page,
                "per_page": records_to_return,
                "total": len(self.mock_data)
            }
        } 