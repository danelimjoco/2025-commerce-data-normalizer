# Commerce Data Normalizer

This project simulates how a unified commerce API might normalize data from different e-commerce platforms like Shopify and WooCommerce, with support for database storage and scheduled updates.

## Features
- Simulates external API calls to Shopify and WooCommerce
- Normalizes product data into a single schema
- Direct database storage of normalized data
- Automatic updates of existing products
- RESTful API for accessing normalized data
- Scheduled data fetching from external APIs

## Architecture

The system uses a direct API integration approach with scheduled updates. This design choice offers several benefits:

- **Platform Independence**: Each platform (Shopify, WooCommerce) has its own dedicated API client, allowing for:
  - Platform-specific data normalization
  - Independent error handling
  - Simplified monitoring and debugging
  - Easy addition of new platforms

- **Data Flow**:
  ```
  External API Client -> Data Normalization -> Products Table -> REST API
  ```
  Each platform's data flows through its own API client, ensuring that:
  - Platform-specific normalization logic remains isolated
  - Processing issues in one platform don't affect others
  - Data from different platforms can be fetched at different rates

## Quick Start

The project includes a Makefile for easy setup and running:

```bash
# Set up everything (venv, dependencies, database)
make setup

# Start all services (API server and scheduler)
make start-all

# Clean up everything
make clean
```

Individual commands:
```bash
# Create virtual environment
make venv

# Install dependencies
make install

# Initialize database
make init-db

# Start API server
make start-api

# Start data scheduler
make start-scheduler

# Make a single API request
python -m external.request shopify  # or woocommerce
```

## API

The API provides a RESTful interface for accessing normalized product data. It's built with FastAPI and includes features like filtering, pagination, and platform-specific queries.

### API Architecture

When you run `uvicorn api.main:app`, the following components work together:

1. **FastAPI Application** (`main.py`):
   - Handles HTTP requests and routing
   - Provides endpoints for product queries
   - Includes automatic API documentation at `/docs`

2. **Database Layer** (`database.py`):
   - Manages PostgreSQL connections
   - Provides session management
   - Handles connection pooling

3. **Data Models**:
   - `schemas.py`: SQLAlchemy models for database operations
   - `models.py`: Pydantic models for request/response validation

4. **Utilities**:
   - `pagination.py`: Handles result pagination
   - `filters.py`: Applies query filters (platform, price, quantity, search)

### External API Integration

The system simulates external API calls through dedicated clients:

1. **Shopify API Client** (`external/shopify.py`):
   - Generates realistic product data
   - Simulates API response times
   - Handles rate limiting
   - Normalizes data into common format

2. **WooCommerce API Client** (`external/woocommerce.py`):
   - Generates realistic product data
   - Simulates API response times
   - Handles rate limiting
   - Normalizes data into common format

3. **Data Scheduler** (`external/scheduler.py`):
   - Runs periodic data fetches
   - Updates existing products
   - Inserts new products
   - Handles errors and retries

### Making API Requests

You can make direct requests to the external APIs:

```bash
# Fetch data from Shopify
python -m external.request shopify

# Fetch data from WooCommerce
python -m external.request woocommerce
```

Each request will:
1. Connect to the simulated API
2. Fetch a random number of products (1-50)
3. Normalize the data
4. Update the database
5. Show detailed operation results

### Scheduled Updates

The scheduler runs periodic updates to keep data fresh:

```bash
# Start the scheduler
python -m external.scheduler
```

The scheduler will:
1. Run every hour
2. Fetch data from both platforms
3. Update existing products
4. Insert new products
5. Show detailed operation logs

## Database Setup

1. Initialize the database:
```bash
make init-db
```

This will:
- Create a postgres user if it doesn't exist
- Create the commerce_data database
- Set up the products table with the required schema

## Database Schema

The `products` table stores normalized product data with the following columns:
- `id`: Auto-incrementing primary key
- `platform`: The e-commerce platform (e.g., 'shopify', 'woocommerce')
- `platform_id`: The product ID from the platform
- `title`: Product title
- `price`: Product price
- `currency`: Currency code (3 letters)
- `quantity`: Available quantity
- `created_at`: Timestamp when the record was created
- `updated_at`: Timestamp when the record was last updated

There is a unique constraint on (platform, platform_id) to prevent duplicates.

## Project Structure
- `external/` → External API integration
  - `shopify.py` → Shopify API client
  - `woocommerce.py` → WooCommerce API client
  - `scheduler.py` → Data fetching scheduler
  - `request.py` → Direct API request utility
  - `base.py` → Base API client class
  - `utils/` → Helper functions
    - `errors.py` → Error handling
    - `rate_limit.py` → Rate limiting utilities
- `database/` → Database setup
  - `init.sh` → Database initialization script
  - `schema.sql` → Database schema definition
- `api/` → REST API components
  - `main.py` → FastAPI application and routes
  - `models.py` → Pydantic models
  - `schemas.py` → SQLAlchemy models
  - `database.py` → Database connection
  - `utils/` → Helper functions
    - `pagination.py` → Pagination logic
    - `filters.py` → Filtering logic

## Dependencies
- psycopg2-binary==2.9.9 (PostgreSQL client)
- python-dotenv==1.0.1 (Environment variable management)
- fastapi==0.109.2 (Web framework)
- uvicorn==0.27.1 (ASGI server)
- sqlalchemy==2.0.27 (ORM)
- pydantic==2.6.1 (Data validation)
- PostgreSQL server