from datetime import datetime
import random
from .base import BaseAPI

class WooCommerceAPI(BaseAPI):
    def __init__(self):
        super().__init__("woocommerce")

    def generate_merchant_metrics(self, merchant_id: str, merchant_name: str) -> dict:
        """Generate WooCommerce-specific metrics and transform to normalized format"""
        # WooCommerce-specific metrics
        wc_metrics = {
            "store_id": merchant_id,
            "store_name": merchant_name,
            "net_sales": round(random.uniform(10000, 1000000), 2),
            "order_volume": random.randint(100, 10000),
            "avg_order_total": round(random.uniform(50, 500), 2),
            "registered_users": random.randint(50, 5000),
            "published_products": random.randint(10, 1000),
            "woocommerce_version": f"{random.randint(5, 8)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "active_plugins": random.randint(5, 30),
            "payment_gateways": random.randint(1, 5)
        }

        # Transform to normalized format
        return {
            "merchant_id": wc_metrics["store_id"],
            "platform": "woocommerce",
            "merchant_name": wc_metrics["store_name"],
            "total_sales": wc_metrics["net_sales"],
            "total_orders": wc_metrics["order_volume"],
            "average_order_value": wc_metrics["avg_order_total"],
            "total_customers": wc_metrics["registered_users"],
            "total_products": wc_metrics["published_products"]
        } 