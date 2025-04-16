from normalizer.base_schema import UnifiedProduct

def normalize_woocommerce(data: dict) -> UnifiedProduct:
    return UnifiedProduct(
        id=str(data["id"]),
        title=data["title"],
        price=float(data["price"]),
        currency=data["currency_code"],
        quantity=int(data["stock_quantity"]),
        created_at=data["date_created"]
    )