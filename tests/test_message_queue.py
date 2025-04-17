import unittest
import json
from unittest.mock import patch, MagicMock
from message_queue.message_queue import MessageQueueHandler

class TestMessageQueue(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_data = {
            'id': 'test_product_1',
            'title': 'Test Product',
            'price': 99.99,
            'currency': 'USD',
            'quantity': 10
        }
        self.platform = 'shopify'

    def test_publish_message(self):
        """Test publishing a message to the queue."""
        with patch('pika.BlockingConnection') as mock_connection:
            # Create mock channel
            mock_channel = MagicMock()
            mock_channel.queue_delete = MagicMock(return_value=None)
            mock_channel.queue_declare = MagicMock(return_value=None)
            mock_channel.basic_publish = MagicMock(return_value=None)
            
            # Create mock connection context manager
            mock_connection_instance = MagicMock()
            mock_connection_instance.channel.return_value = mock_channel
            
            # Set up the context manager chain
            mock_connection.return_value.__enter__.return_value = mock_connection_instance
            
            # Initialize MessageQueueHandler after mocks are set up
            self.queue = MessageQueueHandler()
            
            # Publish test data
            self.queue.publish(self.platform, self.test_data)
            
            # Verify the queue was deleted and redeclared
            mock_channel.queue_delete.assert_called_once_with(queue=self.platform)
            mock_channel.queue_declare.assert_called_once_with(queue=self.platform, durable=True)
            mock_channel.basic_publish.assert_called_once()
            
            # Get the actual message that was published
            call_args = mock_channel.basic_publish.call_args[1]
            published_message = json.loads(call_args['body'])
            
            # Verify the message content
            self.assertEqual(published_message['data'], self.test_data)
            self.assertEqual(published_message['platform'], self.platform)

    def test_consume_message(self):
        """Test consuming a message from the queue."""
        with patch('pika.BlockingConnection') as mock_connection:
            # Create mock channel
            mock_channel = MagicMock()
            mock_channel.queue_delete = MagicMock(return_value=None)
            mock_channel.queue_declare = MagicMock(return_value=None)
            mock_channel.basic_consume = MagicMock(return_value=None)
            mock_channel.start_consuming = MagicMock(return_value=None)
            
            # Create mock connection context manager
            mock_connection_instance = MagicMock()
            mock_connection_instance.channel.return_value = mock_channel
            
            # Set up the context manager chain
            mock_connection.return_value.__enter__.return_value = mock_connection_instance
            
            # Initialize MessageQueueHandler after mocks are set up
            self.queue = MessageQueueHandler()
            
            # Create a test message
            test_message = {
                'data': self.test_data,
                'platform': self.platform
            }
            
            # Simulate message delivery
            def mock_callback(ch, method, properties, body):
                message = json.loads(body)
                self.assertEqual(message['data'], self.test_data)
                self.assertEqual(message['platform'], self.platform)
            
            # Start consuming
            self.queue.consume(mock_callback)
            
            # Verify the queue was deleted and redeclared
            mock_channel.queue_delete.assert_called_once_with(queue=self.platform)
            mock_channel.queue_declare.assert_called_once_with(queue=self.platform, durable=True)

if __name__ == '__main__':
    unittest.main() 