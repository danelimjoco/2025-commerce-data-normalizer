.PHONY: setup venv install init-db start-api stop-api clean request-shopify request-woocommerce start-scheduler start-all

# Python version to use
PYTHON_VERSION = 3.9
VENV_NAME = venv
VENV_BIN = $(VENV_NAME)/bin

setup: venv install init-db activate

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

# Activate virtual environment
activate:
	@echo "Run this command to activate the virtual environment:"
	@echo "source $(VENV_BIN)/activate"

# Start API server in a new terminal
start-api:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && source $(VENV_BIN)/activate && PYTHONPATH=$(PWD) uvicorn api.main:app --reload --port 8001"'
	@echo "\nAPI Documentation URLs:"
	@echo "Swagger UI: http://localhost:8001/docs"
	@echo "ReDoc: http://localhost:8001/redoc"
	@echo "\nAPI Endpoints:"
	@echo "List all merchants: http://localhost:8001/merchant-metrics/"
	@echo "Get specific merchant: http://localhost:8001/merchant-metrics/1"
	@echo "Platform stats: http://localhost:8001/merchant-metrics/platform/shopify/stats"
	@echo "Health check: http://localhost:8001/health"

# Stop API server
stop-api:
	@echo "Stopping API server..."
	@pkill -f "uvicorn api.main:app"
	@echo "API server stopped."

# Make a single request to Shopify API
request-shopify:
	PYTHONPATH=$(PWD) $(VENV_BIN)/python -m external.request shopify

# Make a single request to WooCommerce API
request-woocommerce:
	PYTHONPATH=$(PWD) $(VENV_BIN)/python -m external.request woocommerce

# Start the scheduler in a new terminal
start-scheduler:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && PYTHONPATH=$(PWD) $(VENV_BIN)/python -m external.scheduler"'

# Start all services
start-all:
	$(MAKE) start-api
	$(MAKE) start-scheduler

# Clean up
clean:
	rm -rf $(VENV_NAME)
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__ 