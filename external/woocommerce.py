from datetime import datetime, timedelta
import random
from .base import BaseAPI

class WooCommerceAPI(BaseAPI):
    def __init__(self):
        super().__init__("woocommerce")
        self.mock_data = self._generate_mock_data()

    def _generate_mock_data(self):
        # Generate a unique timestamp-based prefix for this run
        timestamp = int(datetime.utcnow().timestamp())
        return [
            {
                "id": f"woo_{timestamp}_{i}",  # Unique ID with timestamp
                "name": f"WooCommerce Product {i}",
                "price": random.uniform(5, 500),
                "currency": "USD",
                "stock_quantity": random.randint(0, 50),
                "date_modified": datetime.utcnow() - timedelta(minutes=random.randint(0, 30))
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