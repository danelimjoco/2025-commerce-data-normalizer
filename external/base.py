from abc import ABC, abstractmethod
import random
import asyncio
import asyncpg
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseAPI(ABC):
    def __init__(self, platform: str):
        self.platform = platform
        self.db_pool = None
        load_dotenv()
        logger.info(f"Initialized {platform} API")

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
                logger.info(f"Connected to database for {self.platform}")
            except Exception as e:
                logger.error(f"Database connection error for {self.platform}: {str(e)}")
                raise

    @abstractmethod
    def generate_merchant_metrics(self, merchant_id: str, merchant_name: str) -> dict:
        """Generate metrics for a merchant"""
        pass

    async def get_merchant_metrics(self) -> dict:
        """Get merchant metrics from the platform"""
        start_time = asyncio.get_event_loop().time()
        logger.info(f"Starting metrics fetch for {self.platform}")
        
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
        await self.connect_db()
        
        try:
            async with self.db_pool.acquire() as conn:
                # Get existing merchants with their current metrics
                rows = await conn.fetch('''
                    SELECT merchant_id, merchant_name, total_sales, total_orders, 
                           average_order_value, total_customers, total_products,
                           created_at, updated_at
                    FROM merchant_metrics 
                    WHERE platform = $1
                ''', self.platform)
                
                metrics = []
                for row in rows:
                    # Generate new metrics based on existing values
                    new_metrics = self.generate_merchant_metrics(row['merchant_id'], row['merchant_name'])
                    
                    # Apply realistic changes
                    # Total sales should only increase (0-15% growth)
                    new_metrics['total_sales'] = max(
                        float(row['total_sales']),
                        float(row['total_sales']) * (1 + random.uniform(0, 0.15))
                    )
                    
                    # Total orders should only increase (0-10% growth)
                    new_metrics['total_orders'] = max(
                        int(row['total_orders']),
                        int(row['total_orders'] * (1 + random.uniform(0, 0.10)))
                    )
                    
                    # Average order value can fluctuate (-5% to +5%)
                    new_metrics['average_order_value'] = float(row['average_order_value']) * (1 + random.uniform(-0.05, 0.05))
                    
                    # Total customers should only increase (0-5% growth)
                    new_metrics['total_customers'] = max(
                        int(row['total_customers']),
                        int(row['total_customers'] * (1 + random.uniform(0, 0.05)))
                    )
                    
                    # Total products should increase slowly (0-2% growth)
                    new_metrics['total_products'] = max(
                        int(row['total_products']),
                        int(row['total_products'] * (1 + random.uniform(0, 0.02)))
                    )
                    
                    # Preserve created_at
                    new_metrics['created_at'] = row['created_at']
                    
                    metrics.append(new_metrics)
                
                # Occasionally add a new merchant (20% chance)
                if random.random() < 0.2:
                    adjectives = ["Modern", "Coastal", "Urban", "Vintage", "Rustic", "Golden", "Royal", "Elite", 
                                "Premium", "Classic", "Artisan", "Global"]
                    nouns = ["Trading", "Boutique", "Marketplace", "Designs", "Collection", "Goods", "Merchants", 
                            "Emporium", "Commerce", "Exchange", "Retail", "Store"]
                    locations = ["West", "East", "North", "South", "Central", "Pacific", "Atlantic", "Global"]
                    
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        new_merchant_name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(locations)}"
                        new_merchant_id = ''.join(word[0].upper() for word in new_merchant_name.split()) + str(random.randint(100000, 999999))
                        
                        # Check if merchant exists
                        exists = await conn.fetchval(
                            'SELECT EXISTS(SELECT 1 FROM merchant_metrics WHERE merchant_id = $1 OR merchant_name = $2)',
                            new_merchant_id, new_merchant_name
                        )
                        
                        if not exists:
                            new_metrics = self.generate_merchant_metrics(new_merchant_id, new_merchant_name)
                            new_metrics['created_at'] = datetime.utcnow()
                            metrics.append(new_metrics)
                            logger.info(f"Added new merchant {new_merchant_name} ({new_merchant_id})")
                            break
                    else:
                        logger.warning("Failed to generate unique merchant after multiple attempts")
                
                # Update database
                await self.update_metrics(metrics)
                
                duration = asyncio.get_event_loop().time() - start_time
                logger.info(f"Completed {self.platform} metrics fetch in {duration:.2f} seconds")
                return {"data": metrics}
                
        except Exception as e:
            logger.error(f"Error fetching metrics for {self.platform}: {str(e)}")
            raise

    async def update_metrics(self, metrics: list):
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
                logger.info(f"Updated {len(metrics)} metrics for {self.platform}")
        except Exception as e:
            logger.error(f"Error updating metrics for {self.platform}: {str(e)}")
            raise