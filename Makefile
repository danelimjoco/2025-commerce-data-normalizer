.PHONY: setup venv install init-db start-rabbitmq start-consumer start-producer start-all clean test

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

# Start RabbitMQ server
start-rabbitmq:
	brew services start rabbitmq

# Start consumer in a new terminal
start-consumer:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && source $(VENV_BIN)/activate && python -m message_queue.consumer shopify"'

# Start producer in a new terminal
start-producer:
	osascript -e 'tell app "Terminal" to do script "cd $(PWD) && source $(VENV_BIN)/activate && python -m message_queue.producer shopify"'

# Start all services
start-all: start-rabbitmq
	sleep 2  # Wait for RabbitMQ to start
	$(MAKE) start-consumer
	sleep 1  # Wait for consumer to start
	$(MAKE) start-producer

# Clean up
clean:
	rm -rf $(VENV_NAME)
	brew services stop rabbitmq 