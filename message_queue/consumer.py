import sys
import json
import os
import psycopg2
from dotenv import load_dotenv
from message_queue.message_queue import MessageQueueHandler

def normalize_shopify_data(data):
    return {
        "platform": "shopify",
        "platform_id": data["product_id"],
        "title": data["name"],
        "price": float(data["price"]["amount"]),
        "currency": data["price"]["currency"],
        "quantity": data["inventory"],
        "created_at": data["created_at"]
    }

def normalize_woocommerce_data(data):
    return {
        "platform": "woocommerce",
        "platform_id": str(data["id"]),
        "title": data["title"],
        "price": float(data["price"]),
        "currency": data["currency_code"],
        "quantity": data["stock_quantity"],
        "created_at": data["date_created"]
    }

def load_to_database(data):
    load_dotenv()
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "commerce_data"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    
    try:
        with conn.cursor() as cur:
            # Check if product exists using platform and platform_id
            cur.execute(
                "SELECT id FROM products WHERE platform = %s AND platform_id = %s",
                (data["platform"], data["platform_id"])
            )
            result = cur.fetchone()
            
            if result:
                # Update existing product
                cur.execute("""
                    UPDATE products 
                    SET title = %s, price = %s, currency = %s, 
                        quantity = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE platform = %s AND platform_id = %s
                """, (
                    data["title"], data["price"], data["currency"],
                    data["quantity"], data["platform"], data["platform_id"]
                ))
            else:
                # Insert new product
                cur.execute("""
                    INSERT INTO products 
                    (platform, platform_id, title, price, currency, quantity, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """, (
                    data["platform"], data["platform_id"], data["title"], 
                    data["price"], data["currency"], data["quantity"], 
                    data["created_at"]
                ))
            
            conn.commit()
            print(f"Successfully {'updated' if result else 'inserted'} product {data['platform_id']} from {data['platform']}")
            
    except Exception as e:
        print(f"Error loading to database: {e}")
        conn.rollback()
    finally:
        conn.close()

def process_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        platform = method.routing_key
        
        # Normalize data based on platform
        normalizers = {
            'shopify': normalize_shopify_data,
            'woocommerce': normalize_woocommerce_data
        }
        
        if platform not in normalizers:
            print(f"Unknown platform: {platform}")
            return
            
        normalized_data = normalizers[platform](data)
        print(f"Normalized data: {normalized_data}")
        
        # Load to database
        load_to_database(normalized_data)
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python consumer.py <platform>")
        print("Platforms: shopify, woocommerce")
        sys.exit(1)

    platform = sys.argv[1]
    if platform not in ['shopify', 'woocommerce']:
        print("Invalid platform. Choose from: shopify, woocommerce")
        sys.exit(1)

    mq = MessageQueueHandler()
    print(f"Starting consumer for {platform}...")

    try:
        mq.consume(platform, process_message)
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
        mq.close()

if __name__ == "__main__":
    main() 