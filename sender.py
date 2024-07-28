# Example of Script of how to send message to RabbitMQ
import pika
import json

# RabbitMQ Configuration
rabbitmq_host = "localhost"
rabbitmq_user = "user"
rabbitmq_password = "password"
queue_name = "queue_manager"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host,
    credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)

# Send Messages
tasks = [
    {"task": "Task 1", "description": "Description for Task 1","priority": "Low"},
    {"task": "Task 2", "description": "Description for Task 2","priority": "High"},
    {"task": "Task 3", "description": "Description for Task 3","priority": "High"},
]

for task in tasks:
    message = json.dumps(task)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        )
    )
    print(f"Sent {message}")

connection.close()
