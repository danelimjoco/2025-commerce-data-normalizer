# Commerce Data Normalizer

This project simulates how a unified commerce API might normalize data from different e-commerce platforms like Shopify and WooCommerce.

## 💡 Features
- Parses real-world style JSON formats from different platforms
- Normalizes product data into a single schema
- CLI usage for quick testing
- Unit tests included

## 🚀 Usage
```bash
python main.py shopify data/shopify_sample.json
python main.py woocommerce data/woocommerce_sample.json
```

## ✅ Test
```bash
python -m unittest tests/test_normalization.py
```

## 🔧 Structure
- `schemas/` → Format-specific normalizers
- `normalizer/` → Unified schema + controller
- `data/` → Example platform inputs