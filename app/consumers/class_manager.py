import pika
from consumers.class_basic import BaseClassDataQueue
from settings import (
    RABBITMQ_QUEUE_MANAGER,
    RABBITMQ_QUEUE_MONGO
)

class ClassManager(BaseClassDataQueue):
    def __init__(self):
        """
        Initialize the ClassManager with RabbitMQ attributes.
        """
        super().__init__()

    def connect_rabbitmq(self) -> None:
        """
        Connects to RabbitMQ and declares necessary queues.
        """
        super().connect_rabbitmq()
        self.declare_queue(RABBITMQ_QUEUE_MANAGER)
        self.declare_queue(RABBITMQ_QUEUE_MONGO)

    def callback(
        self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        """
        Callback function to process messages received from RabbitMQ.

        Args:
            ch (BlockingChannel): The channel object.
            method (Basic.Deliver): Delivery method.
            properties (BasicProperties): Message properties.
            body (bytes): The message body.
        """
        self.logger.info(f"Received {body}")
        
        try:
            # Forward the message to the MongoDB queue
            self.rabbitmq_channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE_MONGO,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make message persistent
                )
            )
            self.logger.info("Message forwarded to MongoDB queue.")
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_messages(self) -> None:
        """
        Starts the message consumption process.
        """
        self.logger.info("Starting Python app...")
        self.connect_rabbitmq()
        
        self.rabbitmq_channel.basic_consume(
            queue=RABBITMQ_QUEUE_MANAGER,
            on_message_callback=self.callback
        )
        self.logger.info("Waiting for messages...")
        self.rabbitmq_channel.start_consuming()
