import json
import pika
import logging
from typing import Callable, Dict, Any

class MessageQueueHandler:
    def __init__(self):
        """Initialize RabbitMQ connection."""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        
        # Declare queues with consistent properties
        self.channel.queue_declare(queue='shopify', durable=True)
        self.channel.queue_declare(queue='woocommerce', durable=True)

    def publish(self, platform: str, data: Dict[str, Any]) -> None:
        """Publish a message to the specified platform's queue.
        
        Args:
            platform: The platform name (e.g., 'shopify', 'woocommerce')
            data: The data to publish
        """
        try:
            # Publish message with persistence
            self.channel.basic_publish(
                exchange='',
                routing_key=platform,
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2  # make message persistent
                )
            )
            
        except Exception as e:
            logging.error(f"Error publishing message: {str(e)}")
            raise

    def consume(self, platform: str, callback: Callable) -> None:
        """Consume messages from the specified platform's queue.
        
        Args:
            platform: The platform name (e.g., 'shopify', 'woocommerce')
            callback: Function to call when a message is received
        """
        try:
            # Set up consumer
            self.channel.basic_consume(
                queue=platform,
                on_message_callback=callback,
                auto_ack=True
            )
            
            # Start consuming
            print(f"Waiting for messages on {platform} queue...")
            self.channel.start_consuming()
            
        except Exception as e:
            logging.error(f"Error consuming messages: {str(e)}")
            # Don't re-raise the exception to keep the consumer running
            print("Attempting to recover...")
            self.consume(platform, callback)  # Try to restart the consumer

    def close(self) -> None:
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close() 