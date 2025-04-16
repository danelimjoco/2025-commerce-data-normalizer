from normalizer.base_schema import UnifiedProduct

def normalize_shopify(data: dict) -> UnifiedProduct:
    return UnifiedProduct(
        id=data["product_id"],
        title=data["name"],
        price=float(data["price"]["amount"]),
        currency=data["price"]["currency"],
        quantity=data["inventory"],
        created_at=data["created_at"]
    )