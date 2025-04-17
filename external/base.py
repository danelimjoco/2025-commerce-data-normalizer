from abc import ABC, abstractmethod
import random
import asyncio
import asyncpg
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MerchantGenerator:
    """Handles merchant name and ID generation"""
    ADJECTIVES = ["Modern", "Coastal", "Urban", "Vintage", "Rustic", "Golden", "Royal", "Elite", 
                 "Premium", "Classic", "Artisan", "Global"]
    NOUNS = ["Trading", "Boutique", "Marketplace", "Designs", "Collection", "Goods", "Merchants", 
             "Emporium", "Commerce", "Exchange", "Retail", "Store"]
    LOCATIONS = ["West", "East", "North", "South", "Central", "Pacific", "Atlantic", "Global"]

    @staticmethod
    def generate_merchant_info() -> tuple[str, str]:
        """Generate a unique merchant name and ID"""
        name = f"{random.choice(MerchantGenerator.ADJECTIVES)} {random.choice(MerchantGenerator.NOUNS)} {random.choice(MerchantGenerator.LOCATIONS)}"
        merchant_id = ''.join(word[0].upper() for word in name.split()) + str(random.randint(100000, 999999))
        return merchant_id, name

class BaseAPI(ABC):
    def __init__(self, platform: str):
        self.platform = platform
        self.db_pool = None
        load_dotenv()

    async def connect_db(self):
        """Connect to the database"""
        if not self.db_pool:
            try:
                self.db_pool = await asyncpg.create_pool(
                    user=os.getenv('DB_USER', 'postgres'),
                    password=os.getenv('DB_PASSWORD', 'postgres'),
                    database=os.getenv('DB_NAME', 'commerce_data'),
                    host=os.getenv('DB_HOST', 'localhost'),
                    port=os.getenv('DB_PORT', '5432')
                )
            except Exception as e:
                logger.error(f"Database connection error: {str(e)}")
                raise

    @abstractmethod
    def generate_merchant_metrics(self, merchant_id: str, merchant_name: str) -> dict:
        """Generate metrics for a merchant"""
        pass

    def _apply_growth_factors(self, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Apply growth factors to existing metrics"""
        return {
            'total_sales': max(
                float(current_metrics['total_sales']),
                float(current_metrics['total_sales']) * (1 + random.uniform(0, 0.15))
            ),
            'total_orders': max(
                int(current_metrics['total_orders']),
                int(current_metrics['total_orders'] * (1 + random.uniform(0, 0.10)))
            ),
            'average_order_value': float(current_metrics['average_order_value']) * (1 + random.uniform(-0.05, 0.05)),
            'total_customers': max(
                int(current_metrics['total_customers']),
                int(current_metrics['total_customers'] * (1 + random.uniform(0, 0.05)))
            ),
            'total_products': max(
                int(current_metrics['total_products']),
                int(current_metrics['total_products'] * (1 + random.uniform(0, 0.02)))
            )
        }

    async def _create_cross_platform_merchant(self, merchant_id: str, merchant_name: str) -> None:
        """Create a merchant on the other platform"""
        other_platform = 'woocommerce' if self.platform == 'shopify' else 'shopify'
        other_metrics = self.generate_merchant_metrics(merchant_id, merchant_name)
        other_metrics['platform'] = other_platform
        other_metrics['created_at'] = datetime.utcnow()
        await self.update_metrics([other_metrics])
        logger.info(f"Created cross-platform merchant: {merchant_name} ({merchant_id}) on {other_platform}")

    async def get_merchant_metrics(self) -> dict:
        """Get merchant metrics from the platform"""
        start_time = asyncio.get_event_loop().time()
        
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
        await self.connect_db()
        
        try:
            async with self.db_pool.acquire() as conn:
                # Get existing merchants
                rows = await conn.fetch('''
                    SELECT merchant_id, merchant_name, total_sales, total_orders, 
                           average_order_value, total_customers, total_products,
                           created_at, updated_at
                    FROM merchant_metrics 
                    WHERE platform = $1
                ''', self.platform)
                
                metrics = []
                for row in rows:
                    new_metrics = self.generate_merchant_metrics(row['merchant_id'], row['merchant_name'])
                    growth_metrics = self._apply_growth_factors(row)
                    new_metrics.update(growth_metrics)
                    new_metrics['created_at'] = row['created_at']
                    metrics.append(new_metrics)
                
                # Add new merchant (20% chance)
                if random.random() < 0.2:
                    should_create_cross_platform = random.random() < 0.3
                    max_attempts = 3
                    
                    for _ in range(max_attempts):
                        merchant_id, merchant_name = MerchantGenerator.generate_merchant_info()
                        exists = await conn.fetchval(
                            'SELECT EXISTS(SELECT 1 FROM merchant_metrics WHERE merchant_id = $1 OR merchant_name = $2)',
                            merchant_id, merchant_name
                        )
                        
                        if not exists:
                            new_metrics = self.generate_merchant_metrics(merchant_id, merchant_name)
                            new_metrics['created_at'] = datetime.utcnow()
                            metrics.append(new_metrics)
                            
                            if should_create_cross_platform:
                                await self._create_cross_platform_merchant(merchant_id, merchant_name)
                                logger.info(f"Created new merchant: {merchant_name} ({merchant_id}) on {self.platform} (cross-platform)")
                            else:
                                logger.info(f"Created new merchant: {merchant_name} ({merchant_id}) on {self.platform}")
                            break
                    else:
                        logger.warning("Failed to generate unique merchant after multiple attempts")
                
                await self.update_metrics(metrics)
                
                duration = asyncio.get_event_loop().time() - start_time
                logger.info(f"Updated {len(metrics)} metrics in {duration:.2f}s")
                return {"data": metrics}
                
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise

    async def update_metrics(self, metrics: List[Dict[str, Any]]):
        """Update metrics in the database"""
        try:
            async with self.db_pool.acquire() as conn:
                for metric in metrics:
                    await conn.execute('''
                        INSERT INTO merchant_metrics 
                        (merchant_id, platform, merchant_name, total_sales, total_orders, 
                         average_order_value, total_customers, total_products, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP)
                        ON CONFLICT (merchant_id, platform) DO UPDATE SET
                            merchant_name = EXCLUDED.merchant_name,
                            total_sales = EXCLUDED.total_sales,
                            total_orders = EXCLUDED.total_orders,
                            average_order_value = EXCLUDED.average_order_value,
                            total_customers = EXCLUDED.total_customers,
                            total_products = EXCLUDED.total_products,
                            updated_at = CURRENT_TIMESTAMP
                    ''', 
                    metric['merchant_id'],
                    metric['platform'],
                    metric['merchant_name'],
                    metric['total_sales'],
                    metric['total_orders'],
                    metric['average_order_value'],
                    metric['total_customers'],
                    metric['total_products'],
                    metric.get('created_at', datetime.utcnow())
                    )
        except Exception as e:
            logger.error(f"Error updating metrics for {self.platform}: {str(e)}")
            raise