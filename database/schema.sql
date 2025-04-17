-- Create merchant_metrics table
CREATE TABLE IF NOT EXISTS merchant_metrics (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(10) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    merchant_name VARCHAR(255) NOT NULL,
    total_sales DECIMAL(10,2) NOT NULL,
    total_orders INTEGER NOT NULL,
    average_order_value DECIMAL(10,2) NOT NULL,
    total_customers INTEGER NOT NULL,
    total_products INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(merchant_id, platform)  -- Ensure a merchant can only have one record per platform
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_merchant_metrics_platform ON merchant_metrics(platform);
CREATE INDEX IF NOT EXISTS idx_merchant_metrics_merchant_id ON merchant_metrics(merchant_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_merchant_metrics_updated_at
    BEFORE UPDATE ON merchant_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 