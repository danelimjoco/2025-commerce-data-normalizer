-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    platform_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE(platform, platform_id)
);

-- Create index on platform and platform_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_products_platform_id ON products(platform, platform_id); 