import pika
import pymongo
import json
import time
from typing import Optional
from consumers.class_basic import BaseClassDataQueue
from settings import (
    RABBITMQ_QUEUE_MONGO,
    MONGO_HOSTNAME,
    MONGO_COLLECTION,
    MONGO_DATABASE,
    MONGO_PORT
)

class MongoDBClient(BaseClassDataQueue):
    def __init__(self):
        """
        Initialize the MongoDBClient with RabbitMQ and MongoDB attributes.
        """
        super().__init__()
        self.mongo_client: Optional[pymongo.MongoClient] = None
        self.mongo_collection: Optional[pymongo.collection.Collection] = None

    def connect_mongodb(self) -> None:
        """
        Connects to MongoDB and selects the specified database and collection.
        
        This method attempts to establish a connection to MongoDB, retrying every 5 seconds
        if it fails due to a connection error.
        """
        while True:
            try:
                self.mongo_client = pymongo.MongoClient(MONGO_HOSTNAME, MONGO_PORT)
                db = self.mongo_client[MONGO_DATABASE]
                self.mongo_collection = db[MONGO_COLLECTION]
                self.logger.info("Connected to MongoDB.")
                break
            except pymongo.errors.ConnectionFailure as e:
                self.logger.error(f"MongoDB Connection Error: {e}")
                self.logger.info("Retrying connection to MongoDB...")
                time.sleep(5)  # Wait before retrying

    def connect_rabbitmq(self) -> None:
        """
        Connects to RabbitMQ and declares a queue for MongoDB.
        """
        super().connect_rabbitmq()
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

        Decodes the JSON message and inserts it into MongoDB. Acknowledges the
        message after successful processing.

        Args:
            ch (BlockingChannel): The channel object.
            method (Basic.Deliver): Delivery method.
            properties (BasicProperties): Message properties.
            body (bytes): The message body.
        """
        self.logger.info(f"Received {body}")
        
        try:
            data = json.loads(body)
            result = self.mongo_collection.insert_one(data)
            self.logger.info(f"Data saved in MongoDB with ID {result.inserted_id}")
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {e}")  
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_messages(self) -> None:
        """
        Starts the message consumption process.
        """
        self.logger.info("Starting MongoDB client...")
        self.connect_rabbitmq()
        self.connect_mongodb()  # Ensure MongoDB is connected before starting consumption
        
        self.rabbitmq_channel.basic_consume(queue=RABBITMQ_QUEUE_MONGO, on_message_callback=self.callback)
        self.logger.info("Prepared to save messages...")
        self.rabbitmq_channel.start_consuming()
