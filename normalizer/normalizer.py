import json
from schemas.shopify_schema import normalize_shopify
from schemas.woocommerce_schema import normalize_woocommerce

def normalize(platform: str, filepath: str):
    with open(filepath, "r") as f:
        raw_data = json.load(f)

    if platform == "shopify":
        return normalize_shopify(raw_data).to_dict()
    elif platform == "woocommerce":
        return normalize_woocommerce(raw_data).to_dict()
    else:
        raise ValueError("Unsupported platform")