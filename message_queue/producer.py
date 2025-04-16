import sys
import random
import time
from message_queue.message_queue import MessageQueueHandler

def generate_shopify_data():
    return {
        "product_id": f"prod_{random.randint(1000, 9999)}",
        "name": f"Product {random.randint(1, 100)}",
        "price": {
            "amount": str(round(random.uniform(10, 1000), 2)),
            "currency": "USD"
        },
        "inventory": random.randint(0, 100),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def generate_woocommerce_data():
    return {
        "id": random.randint(1000, 9999),
        "title": f"Product {random.randint(1, 100)}",
        "price": round(random.uniform(10, 1000), 2),
        "currency_code": "USD",
        "stock_quantity": random.randint(0, 100),
        "date_created": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python producer.py <platform>")
        print("Platforms: shopify, woocommerce")
        sys.exit(1)

    platform = sys.argv[1]
    generators = {
        'shopify': generate_shopify_data,
        'woocommerce': generate_woocommerce_data
    }

    if platform not in generators:
        print("Invalid platform. Choose from: shopify, woocommerce")
        sys.exit(1)

    mq = MessageQueueHandler()
    print(f"Starting producer for {platform}...")

    try:
        while True:
            data = generators[platform]()
            print(f"Publishing data: {data}")
            mq.publish(platform, data)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nShutting down producer...")
        mq.close()

if __name__ == "__main__":
    main() 