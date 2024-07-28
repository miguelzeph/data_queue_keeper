# Data Queue Keeper

**Data Queue Keeper** is a project designed to integrate messaging services and data storage using Docker Compose. It consists of a Python application that consumes messages from a RabbitMQ queue and stores the data in a MongoDB database. The system consists of three main components:

- **RabbitMQ**: Used for managing message queues.
- **MongoDB**: Used for persistent data storage.
- **Python Application**: Consumes messages from the RabbitMQ queue and saves them in MongoDB.



# Prerequisites
Before setting up the project, ensure you have the following tools installed on your system:

- Docker/Docker Compose
- Python 3.11 or higher

# Project Structure
The project directory structure is organized as follows:
```bash
.
├── app # Main directory of the Python application
│   ├── consumers # Contains the code responsible for consuming messages from RabbitMQ.
│   │   ├── manager.py # Implements the logic for connecting to RabbitMQ and MongoDB, as well as processing messages
│   └── main.py # Main file that starts the application.
│   └── settings.py # Contains the settings and environment variables for the application.
├── config.yml # onfiguration file that contains the definitions for RabbitMQ, MongoDB, and logger.
├── docker-compose.yml # Docker Compose configuration file for orchestrating the containers.
├── Dockerfile_python_manager # Defines the Docker environment for the Python application.
├── README.md # Project documentation.
├── requirements.txt # List of Python dependencies required for the project
└── sender.py # Script used to send messages to the RabbitMQ queue for testing purposes.
```



# Environment Setup

1. Clone the Repository

Clone the project repository to your local working directory:

```bash
git clone LINKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cd data-queue-keeper
```

2. Create a Python Virtual Environment (optional but recommended)
It is a good practice to create a virtual environment to manage the project's dependencies:

```bash
# create virtual env
virtualenv --python=<your_python_path> <your_env_name>

# Activate virtual env
source ./env/bin/activate #  On Windows, use `venv\Scripts\activate`
```

3. Installing the dependecies, execute:
```bash
pip install -r requirements.txt
```

# Running the Application

To run the project, follow the steps below:

1. Start the Containers with Docker Compose
Run the following command to build and start the containers:

```bash
docker-compose up --build
```

This command will download the necessary images, build the Python application's image, and start all the containers defined in the docker-compose.yml.

2. Access the **RabbitMQ Management Interface**
Open a web browser and access the RabbitMQ management interface at `http://localhost:15672`. Use the credentials defined in the docker-compose.yml (**user** / **password**). Now you can check the flow of messages for queues.

3. Send Messages to **RabbitMQ** using **Python Script**.

To test the system, you can run the `sender.py` script, which sends messages to RabbitMQ:

```bash
python sender.py
```
This script will send JSON messages to the RabbitMQ queue, which will be processed by the Python application and stored in MongoDB.

4. Send Messages to **RabbitMQ** using **RabbitMQ Management Interface**.

- Go to **queues and Streams**
- Click on the queue name **queue_manager**
- Scroll down to **Publish message**
- Write a **JSON message** (always use JSON format) whatever you want, for instance:
```python
{"title":"your title...", "message":"Write here your message....", "year":2024}
```

# Playing with Containers

In this section, we'll explore the resilience of the RabbitMQ messaging system by intentionally stopping the Python manager app container. This demonstration will show you how RabbitMQ handles messages when the consumer is inactive and what happens when it resumes.

1. Stop the Python Manager App Container. To simulate a situation where the consumer is unavailable, we'll stop the python_manager container. Open a new terminal and execute the following command:

```bash
docker-compose stop python_manager
```
This will stop the container responsible for processing messages from RabbitMQ and storing them in MongoDB.

2. Send Messages to RabbitMQ

With the consumer container stopped, let's send some messages to RabbitMQ. You can do this using your sender.py script:

```bash
python sender.py
```

At this point, the messages are being sent to RabbitMQ, but since the consumer is not running, they will be held in the queue.

3. Verify Message Persistence

You can log in to the RabbitMQ management interface to verify that messages are being queued. Open a browser and go to http://localhost:15672. Log in with your credentials (user/password) and navigate to the Queues tab to see your queue and the number of messages waiting (check the Graphics).

This illustrates the power of RabbitMQ's message persistence feature, ensuring no data is lost even when the consumer is temporarily down.

4. Start the Python Manager App Container Again

Now, let's restart the python_manager container to process the messages:

```bash
docker-compose start python_manager
```

Once the container is up and running, it will begin consuming the messages queued in RabbitMQ and storing them in MongoDB.

5. Finally, check MongoDB for processed messages

