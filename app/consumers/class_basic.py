import pika
import time
from typing import Optional

from settings import (
    RABBITMQ_HOSTNAME,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    get_logger
)

class BaseClassDataQueue:
    def __init__(self):
        """
        Initialize the BaseRabbitMQClient with RabbitMQ attributes.
        """
        self.logger = get_logger(__name__)
        self.rabbitmq_connection: Optional[pika.BlockingConnection] = None
        self.rabbitmq_channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None

    def connect_rabbitmq(self) -> None:
        """
        Connects to RabbitMQ and declares the necessary queues.
        """
        while True:
            try:
                self.rabbitmq_connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOSTNAME,
                        credentials=pika.PlainCredentials(
                            RABBITMQ_USER,
                            RABBITMQ_PASSWORD
                        )
                    )
                )
                self.rabbitmq_channel = self.rabbitmq_connection.channel()
                self.logger.info("Connected to RabbitMQ.")
                break
            except pika.exceptions.AMQPConnectionError as e:
                self.logger.error(f"RabbitMQ Connection Error: {e}")
                self.logger.info("Waiting for connection to RabbitMQ...")
                time.sleep(5)
    
    def declare_queue(self, queue_name: str) -> None:
        """
        Declares a RabbitMQ queue.

        Args:
            queue_name (str): The name of the queue to declare.
        """
        self.rabbitmq_channel.queue_declare(queue=queue_name, durable=True)
