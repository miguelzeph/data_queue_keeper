from consumers.class_mongo import MongoDBClient

if __name__ == "__main__":

    # Create an Instance
    mongo_client = MongoDBClient()
    mongo_client.consume_messages()


# from consumers.manager import ClassManager


# if __name__ == "__main__":
    
#     # Initiate the message consumption process to
#     # continuously listen for and process messages
#     manager = ClassManager()
#     manager.consume_messages()
