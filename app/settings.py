import logging
from klein_config import get_config

# Get config from env var
config = get_config()

####### RabbitMQ Settings ########
RABBITMQ_HOSTNAME = config.get("rabbitmq.hostname")
RABBITMQ_USER = config.get("rabbitmq.user")
RABBITMQ_PASSWORD = config.get("rabbitmq.password")
RABBITMQ_QUEUE_MANAGER = config.get("rabbitmq.queue.manager")
RABBITMQ_QUEUE_MONGO = config.get("rabbitmq.queue.mongo")

####### MongoDB Settings ########
MONGO_HOSTNAME = config.get("mongo.hostname")
MONGO_PORT = config.get("mongo.port")
MONGO_DATABASE = config.get("mongo.database")
MONGO_COLLECTION = config.get("mongo.collection")

####### Logger Settings #########
logging.basicConfig(
    level=config.get("logger.level"),
    handlers=[
        logging.StreamHandler(),
    ],
)

def get_logger(module_name: str) -> logging.Logger:
    """Get a logger instance for the specified module.

    This function initializes a logger for the specified module name and returns
    the logger instance. The logger can be used to output log messages to various
    destinations, such as the console, files, or other handlers configured in
    the logging system.
    """
    return logging.getLogger(module_name)
