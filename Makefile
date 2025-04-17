.PHONY: setup venv install init-db start-rabbitmq start-consumer start-producer start-api start-all clean request-shopify request-woocommerce start-scheduler

# Python version to use
PYTHON_VERSION = 3.9
VENV_NAME = venv
VENV_BIN = $(VENV_NAME)/bin

setup: venv install init-db

# Create virtual environment
venv:
	python -m venv $(VENV_NAME)
	$(VENV_BIN)/pip install --upgrade pip

# Install dependencies
install:
	$(VENV_BIN)/pip install -r requirements.txt

# Initialize database
init-db:
	chmod +x database/init.sh
	./database/init.sh

# Start API server in a new terminal
start-api:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && source $(VENV_BIN)/activate && PYTHONPATH=$(PWD) uvicorn api.main:app --reload --port 8001"'

# Make a single request to Shopify API
request-shopify:
	PYTHONPATH=$(PWD) $(VENV_BIN)/python -m external.request shopify

# Make a single request to WooCommerce API
request-woocommerce:
	PYTHONPATH=$(PWD) $(VENV_BIN)/python -m external.request woocommerce

# Start the scheduler in a new terminal
start-scheduler:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && source $(VENV_BIN)/activate && PYTHONPATH=$(PWD) python -m external.scheduler"'

# Start all services
start-all:
	$(MAKE) start-api

# Clean up
clean:
	rm -rf $(VENV_NAME)
	brew services stop rabbitmq 