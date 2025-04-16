# Commerce Data Normalizer

This project simulates how a unified commerce API might normalize data from different e-commerce platforms like Shopify and WooCommerce, with support for real-time processing and database storage.

## Features
- Parses real-world style JSON formats from different platforms
- Normalizes product data into a single schema
- Real-time data processing using RabbitMQ
- Direct database storage of normalized data
- Automatic updates of existing products
- RESTful API for accessing normalized data

## Architecture

The system uses a message queue architecture with separate queues for each e-commerce platform. This design choice offers several benefits:

- **Platform Independence**: Each platform (Shopify, WooCommerce) has its own dedicated pipeline, allowing for:
  - Independent scaling of processing capacity
  - Platform-specific error handling
  - Simplified monitoring and debugging
  - Easy addition of new platforms

- **Data Flow**:
  ```
  Platform Producer -> Platform Queue -> Platform Consumer -> Products Table -> REST API
  ```
  Each platform's data flows through its own queue, ensuring that:
  - Platform-specific normalization logic remains isolated
  - Processing issues in one platform don't affect others
  - Data from different platforms can be processed at different rates

## Quick Start

The project includes a Makefile for easy setup and running:

```bash
# Set up everything (venv, dependencies, database)
make setup

# Start all services (RabbitMQ, consumer, producer, API)
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

# Start RabbitMQ
make start-rabbitmq

# Start consumer in new terminal
make start-consumer

# Start producer in new terminal
make start-producer

# Start API server in new terminal
make start-api
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

### Understanding Async Functions

The API uses async functions (`async def`) for endpoints, but it's important to understand when async is beneficial:

1. **When Async is Valuable**:
   ```python
   async def get_product_with_external_data():
       # These operations can run in parallel
       product_task = db.query(Product)        # Database query
       inventory_task = get_inventory()        # External API call
       reviews_task = get_reviews()            # Another API call
       
       # Wait for all to complete
       product = await product_task
       inventory = await inventory_task
       reviews = await reviews_task
       
       return combine_data(product, inventory, reviews)
   ```
   - Multiple independent operations that can run simultaneously
   - External API calls that don't depend on each other
   - File operations that can happen in parallel
   - Background tasks that don't block the main flow

2. **When Async is Less Beneficial**:
   ```python
   async def get_products():
       # These operations must happen in sequence
       query = db.query(Product)          # Step 1
       query = apply_filters(query)       # Step 2 (needs Step 1)
       items = paginate(query)            # Step 3 (needs Step 2)
       return items                       # Step 4 (needs Step 3)
   ```
   - Sequential operations where each step depends on the previous
   - Simple database queries without external calls
   - Operations that must complete in order

3. **Why We Use Async Anyway**:
   - FastAPI is built on an async framework (Starlette)
   - It's a convention that makes the code ready for future async operations
   - The framework handles request/response cycles more efficiently
   - Makes it easier to add truly async operations later

The API follows RESTful principles and provides endpoints for:
- Listing products with filtering and pagination
- Getting individual products by ID
- Querying platform-specific products
- Health monitoring

### API Documentation

The API is available at `http://localhost:8001` with interactive documentation at `http://localhost:8001/docs`.

### Endpoints

1. **List Products**
   ```
   GET /api/products
   ```
   Query Parameters:
   - `page`: Page number (default: 1)
   - `per_page`: Items per page (default: 20)
   - `platform`: Filter by platform
   - `min_price`: Minimum price
   - `max_price`: Maximum price
   - `min_quantity`: Minimum quantity
   - `search`: Search in product titles

2. **Get Single Product**
   ```
   GET /api/products/{id}
   ```

3. **Get Products by Platform**
   ```
   GET /api/products/platform/{platform}
   ```
   Query Parameters:
   - `page`: Page number (default: 1)
   - `per_page`: Items per page (default: 20)

4. **Health Check**
   ```
   GET /health
   ```

## Database Setup

1. Initialize the database:
```bash
make init-db
```

This will:
- Create a postgres user if it doesn't exist
- Create the commerce_data database
- Set up the products table with the required schema

## Real-time Processing
The real-time processing system consists of three main components:

1. **Message Queue (RabbitMQ)**
   - Acts as a message broker between producers and consumers
   - Ensures reliable message delivery
   - Handles message routing to appropriate queues
   - Maintains message order and persistence

2. **Producer**
   - Simulates real-time data from e-commerce platforms
   - Generates random product data every 2 seconds
   - Formats data according to platform-specific schemas
   - Publishes messages to the appropriate queue
   - Example usage:
   ```bash
   python -m message_queue.producer shopify
   ```

3. **Consumer**
   - Listens for incoming messages on platform-specific queues
   - Normalizes the received data into a unified format
   - Directly loads data into PostgreSQL database
   - Automatically updates existing products
   - Handles errors and acknowledgments
   - Example usage:
   ```bash
   python -m message_queue.consumer shopify
   ```

To start real-time processing:

1. Start RabbitMQ server:
```bash
brew services start rabbitmq  # macOS
```

2. Start a consumer for a specific platform:
```bash
python -m message_queue.consumer shopify
```

3. Start a producer to simulate data:
```bash
python -m message_queue.producer shopify
```

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
- `message_queue/` → Real-time processing components
  - `message_queue.py` → RabbitMQ handler
  - `consumer.py` → Message consumer (loads data to database)
  - `producer.py` → Data generator
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
- pika==1.3.2 (RabbitMQ client)
- psycopg2-binary==2.9.9 (PostgreSQL client)
- python-dotenv==1.0.1 (Environment variable management)
- fastapi==0.109.2 (Web framework)
- uvicorn==0.27.1 (ASGI server)
- sqlalchemy==2.0.27 (ORM)
- pydantic==2.6.1 (Data validation)
- RabbitMQ server
- PostgreSQL server