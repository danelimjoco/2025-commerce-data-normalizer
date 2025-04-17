from datetime import datetime
import random
from .base import BaseAPI

class ShopifyAPI(BaseAPI):
    def __init__(self):
        super().__init__("shopify")

    def generate_merchant_metrics(self, merchant_id: str, merchant_name: str) -> dict:
        """Generate Shopify-specific metrics and transform to normalized format"""
        # Shopify-specific metrics
        shopify_metrics = {
            "shop_id": merchant_id,
            "shop_name": merchant_name,
            "gross_sales": round(random.uniform(10000, 1000000), 2),
            "orders_count": random.randint(100, 10000),
            "average_order_amount": round(random.uniform(50, 500), 2),
            "customer_count": random.randint(50, 5000),
            "product_count": random.randint(10, 1000),
            "abandoned_cart_rate": round(random.uniform(0.1, 0.3), 2),
            "shopify_plus": random.choice([True, False]),
            "app_usage": random.randint(1, 20)
        }

        # Transform to normalized format
        return {
            "merchant_id": shopify_metrics["shop_id"],
            "platform": "shopify",
            "merchant_name": shopify_metrics["shop_name"],
            "total_sales": shopify_metrics["gross_sales"],
            "total_orders": shopify_metrics["orders_count"],
            "average_order_value": shopify_metrics["average_order_amount"],
            "total_customers": shopify_metrics["customer_count"],
            "total_products": shopify_metrics["product_count"]
        } 