from datetime import datetime, timedelta
import asyncio
from .shopify import ShopifyAPI
from .woocommerce import WooCommerceAPI
from api.database import get_db
from api.schemas import Product

class DataFetcher:
    def __init__(self):
        self.apis = {
            "shopify": ShopifyAPI(),
            "woocommerce": WooCommerceAPI()
        }

    async def fetch_all(self):
        """Fetch data from all platforms."""
        for platform, api in self.apis.items():
            try:
                await self._fetch_platform(platform, api)
            except Exception as e:
                print(f"Error fetching {platform}: {e}")

    async def _fetch_platform(self, platform: str, api):
        """Fetch and store data for a specific platform."""
        db = next(get_db())
        try:
            # Get all products
            response = await api.get_products()
            products = response["data"]
            print(f"\nFetched {len(products)} products from {platform}")
            
            # Track updates vs inserts
            updates = 0
            inserts = 0
            
            # Store products
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
            
            # Commit changes
            db.commit()
            print(f"Database operations for {platform}:")
            print(f"  - Updated {updates} existing products")
            print(f"  - Inserted {inserts} new products")
            print(f"  - Total products processed: {updates + inserts}")
            
            # Verify the changes
            total_in_db = db.query(Product).filter_by(platform=platform).count()
            print(f"  - Total products in database for {platform}: {total_in_db}")
            
        except Exception as e:
            print(f"Error fetching {platform}: {e}")
            db.rollback()
        finally:
            db.close()

async def run_scheduler():
    """Run the scheduler in a loop."""
    print("\n" + "="*50)
    print("Starting E-commerce Data Scheduler")
    print("="*50)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scheduler will run every hour")
    print("="*50 + "\n")
    
    fetcher = DataFetcher()
    while True:
        print("\n" + "-"*50)
        print(f"Starting scheduled fetch at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*50)
        
        await fetcher.fetch_all()
        
        next_run = datetime.now() + timedelta(hours=1)
        print("\n" + "-"*50)
        print(f"Fetch completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next fetch scheduled for {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*50 + "\n")
        
        await asyncio.sleep(3600)  # Run every hour

if __name__ == "__main__":
    try:
        asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        print("\n" + "="*50)
        print("Scheduler stopped by user")
        print("="*50) 