# Commerce Data Normalizer

This project simulates how a unified commerce API might normalize data from different e-commerce platforms like Shopify and WooCommerce, with support for real-time processing and database storage.

## Features
- Parses real-world style JSON formats from different platforms
- Normalizes product data into a single schema
- Real-time data processing using RabbitMQ
- Direct database storage of normalized data
- Automatic updates of existing products

## Architecture

The system uses a message queue architecture with separate queues for each e-commerce platform. This design choice offers several benefits:

- **Platform Independence**: Each platform (Shopify, WooCommerce) has its own dedicated pipeline, allowing for:
  - Independent scaling of processing capacity
  - Platform-specific error handling
  - Simplified monitoring and debugging
  - Easy addition of new platforms

- **Data Flow**:
  ```
  Platform Producer -> Platform Queue -> Platform Consumer -> Products Table
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

# Start all services (RabbitMQ, consumer, producer)
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

## Dependencies
- pika==1.3.1 (RabbitMQ client)
- psycopg2-binary==2.9.9 (PostgreSQL client)
- python-dotenv==1.0.0 (Environment variable management)
- RabbitMQ server
- PostgreSQL server