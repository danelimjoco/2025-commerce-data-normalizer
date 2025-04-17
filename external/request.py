import asyncio
import argparse
from .woocommerce import WooCommerceAPI
from .shopify import ShopifyAPI
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fetch_metrics(platform: str):
    """Fetch metrics for a specific platform"""
    try:
        logger.info(f"Starting metrics fetch for {platform}")
        api = ShopifyAPI() if platform.lower() == 'shopify' else WooCommerceAPI()
        await api.get_merchant_metrics()
        logger.info(f"Successfully completed metrics fetch for {platform}")
    except Exception as e:
        logger.error(f"Error fetching metrics for {platform}: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Fetch merchant metrics for a specific platform')
    parser.add_argument('platform', choices=['shopify', 'woocommerce'], 
                       help='Platform to fetch metrics for')
    args = parser.parse_args()
    
    try:
        asyncio.run(fetch_metrics(args.platform))
    except KeyboardInterrupt:
        logger.info("Metrics fetch interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 