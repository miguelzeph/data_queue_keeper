import pika
import pymongo
import json
import time
from settings import (
    RABBITMQ_HOSTNAME,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    RABBITMQ_QUEUE_MANAGER,
    MONGO_HOSTNAME,
    MONGO_COLLECTION,
    MONGO_DATABASE,
    MONGO_PORT,
    get_logger
)

class ClassManager:
    def __init__(self):
        # Logger
        self.logger = get_logger(__name__)

        # RabbitMQ attributes
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None

        # MongoDB attributes
        self.mongo_client = None
        self.mongo_collection = None

    def connect_rabbitmq(self):
        while True:
            try:
                self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=RABBITMQ_HOSTNAME,
                    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
                ))
                self.rabbitmq_channel = self.rabbitmq_connection.channel()
                self.logger.info("Connected to RabbitMQ.")
                self.rabbitmq_channel.queue_declare(queue=RABBITMQ_QUEUE_MANAGER, durable=True)
                break
            except pika.exceptions.AMQPConnectionError as e:
                self.logger.error(f"RabbitMQ Connection Error: {e}")
                self.logger.info("Waiting for connection to RabbitMQ...")
                time.sleep(5)

    def connect_mongodb(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_HOSTNAME, MONGO_PORT)
            db = self.mongo_client[MONGO_DATABASE]
            self.mongo_collection = db[MONGO_COLLECTION]
            self.logger.info("Connected to MongoDB.")
        except pymongo.errors.ConnectionFailure as e:
            self.logger.error(f"MongoDB Connection Error: {e}")
            return False
        return True

    def callback(self, ch, method, properties, body):
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

    def consume_messages(self):
        self.logger.info("Starting Python app...")
        self.connect_rabbitmq()
        if not self.connect_mongodb():
            return
        
        self.rabbitmq_channel.basic_consume(queue=RABBITMQ_QUEUE_MANAGER, on_message_callback=self.callback)
        self.logger.info("Waiting for messages...")
        self.rabbitmq_channel.start_consuming()
