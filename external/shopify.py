from datetime import datetime
import random
from .base import BaseAPI

class ShopifyAPI(BaseAPI):
    def __init__(self):
        super().__init__("shopify")

    def generate_merchant_metrics(self, merchant_id: str, merchant_name: str) -> dict:
        """Generate metrics for a Shopify merchant"""
        return {
            "merchant_id": merchant_id,
            "platform": "shopify",
            "merchant_name": merchant_name,
            "total_sales": round(random.uniform(10000, 1000000), 2),
            "total_orders": random.randint(100, 10000),
            "average_order_value": round(random.uniform(50, 500), 2),
            "total_customers": random.randint(50, 5000),
            "total_products": random.randint(10, 1000)
        } 