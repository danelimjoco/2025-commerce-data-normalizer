import asyncio
from datetime import datetime, timedelta
from .shopify import ShopifyAPI
from .woocommerce import WooCommerceAPI

class DataFetcher:
    def __init__(self):
        self.apis = {
            'shopify': ShopifyAPI(),
            'woocommerce': WooCommerceAPI()
        }

    async def fetch_all(self):
        """Fetch metrics from all platforms"""
        for platform, api in self.apis.items():
            try:
                print(f"\nFetching metrics from {platform}...")
                response = await api.get_merchant_metrics()
                print(f"Successfully fetched {len(response['data'])} merchant metrics from {platform}")
            except Exception as e:
                print(f"Error fetching metrics for {platform}: {str(e)}")

async def run_scheduler():
    """Run the data fetcher every minute"""
    fetcher = DataFetcher()
    while True:
        print(f"\nStarting scheduled fetch at {datetime.now()}")
        await fetcher.fetch_all()
        print(f"\nCompleted fetch at {datetime.now()}")
        print(f"Next fetch scheduled for {datetime.now() + timedelta(minutes=1)}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    print("Starting metrics fetcher scheduler...")
    print("Press Ctrl+C to stop")
    try:
        asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
