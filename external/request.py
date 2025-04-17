import asyncio
import sys
from datetime import datetime
from external.shopify import ShopifyAPI
from external.woocommerce import WooCommerceAPI
from api.database import get_db
from api.schemas import Product

async def make_request(platform: str):
    """Make a single request to the specified platform and store in database."""
    if platform.lower() == "shopify":
        api = ShopifyAPI()
    elif platform.lower() == "woocommerce":
        api = WooCommerceAPI()
    else:
        print(f"Unknown platform: {platform}")
        return

    try:
        # Get all products
        response = await api.get_products()
        products = response["data"]
        print(f"\nFetched {len(products)} products from {platform}")
        
        # Track updates vs inserts
        updates = 0
        inserts = 0
        
        # Store in database
        db = next(get_db())
        try:
            for product_data in products:
                # First try to get existing product
                existing_product = db.query(Product).filter_by(
                    platform=platform,
                    platform_id=product_data["id"]
                ).first()
                
                if existing_product:
                    # Update existing product
                    existing_product.title = product_data.get("title") or product_data.get("name")
                    existing_product.price = product_data["price"]
                    existing_product.currency = product_data["currency"]
                    existing_product.quantity = product_data.get("quantity") or product_data.get("stock_quantity")
                    existing_product.updated_at = datetime.utcnow()
                    updates += 1
                else:
                    # Create new product
                    product = Product(
                        platform=platform,
                        platform_id=product_data["id"],
                        title=product_data.get("title") or product_data.get("name"),
                        price=product_data["price"],
                        currency=product_data["currency"],
                        quantity=product_data.get("quantity") or product_data.get("stock_quantity"),
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(product)
                    inserts += 1
            
            db.commit()
            print(f"Database operations for {platform}:")
            print(f"  - Updated {updates} existing products")
            print(f"  - Inserted {inserts} new products")
            print(f"  - Total products processed: {updates + inserts}")
            
            # Verify the changes
            total_in_db = db.query(Product).filter_by(platform=platform).count()
            print(f"  - Total products in database for {platform}: {total_in_db}")
            
        except Exception as e:
            print(f"Database error: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m external.request <platform>")
        print("Platforms: shopify, woocommerce")
        sys.exit(1)
    
    platform = sys.argv[1]
    asyncio.run(make_request(platform)) 