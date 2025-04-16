import unittest
from schemas.shopify_schema import normalize_shopify
from schemas.woocommerce_schema import normalize_woocommerce

class TestNormalization(unittest.TestCase):
    def test_shopify(self):
        data = {
            "product_id": "abc123",
            "name": "Cool Hoodie",
            "price": {"amount": "39.99", "currency": "USD"},
            "inventory": 50,
            "created_at": "2024-12-01T10:00:00Z"
        }
        normalized = normalize_shopify(data).to_dict()
        self.assertEqual(normalized["id"], "abc123")
        self.assertEqual(normalized["price"], 39.99)

    def test_woocommerce(self):
        data = {
            "id": 555,
            "title": "Cool Hoodie",
            "price": 39.99,
            "currency_code": "USD",
            "stock_quantity": 50,
            "date_created": "2024-12-01T10:00:00Z"
        }
        normalized = normalize_woocommerce(data).to_dict()
        self.assertEqual(normalized["id"], "555")
        self.assertEqual(normalized["price"], 39.99)

if __name__ == '__main__':
    unittest.main()