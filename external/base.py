from abc import ABC, abstractmethod
import random
import asyncio

class BaseAPI(ABC):
    def __init__(self, platform: str):
        self.platform = platform
        self.mock_data = self._generate_mock_data()

    @abstractmethod
    def _generate_mock_data(self):
        """Generate mock data for the platform"""
        pass

    async def get_products(self) -> dict:
        """Get all products from the platform."""
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return {
            "data": self.mock_data
        } 