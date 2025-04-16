#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create postgres user if it doesn't exist
createuser -s postgres 2>/dev/null || true

# Create the database if it doesn't exist
createdb -U postgres commerce_data 2>/dev/null || true

# Create the schema using the full path
psql -U postgres -d commerce_data -f "$SCRIPT_DIR/schema.sql"

echo "Database setup complete!" 