from consumers.manager import ClassManager


if __name__ == "__main__":
    
    # Initiate the message consumption process to
    # continuously listen for and process messages
    manager = ClassManager()
    manager.consume_messages()
