#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create postgres user if it doesn't exist
createuser -s postgres 2>/dev/null || true

# Create the database if it doesn't exist
createdb -U postgres commerce_data 2>/dev/null || true

# Create the schema using the full path
psql -U postgres -d commerce_data -f "$SCRIPT_DIR/schema.sql"

# Create sample data only after schema is created
psql -U postgres -d commerce_data << EOF
INSERT INTO merchant_metrics (merchant_id, platform, merchant_name, total_sales, total_orders, average_order_value, total_customers, total_products)
VALUES 
    ('SHOP001', 'shopify', 'Shopify Store 1', 100000.00, 500, 200.00, 300, 100),
    ('SHOP002', 'shopify', 'Shopify Store 2', 50000.00, 250, 200.00, 150, 50),
    ('WOO001', 'woocommerce', 'Woo Store 1', 75000.00, 300, 250.00, 200, 75),
    ('WOO002', 'woocommerce', 'Woo Store 2', 25000.00, 100, 250.00, 80, 25);
EOF

echo "Database setup complete!" 