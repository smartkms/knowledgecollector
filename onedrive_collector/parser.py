from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient("mongodb://root:example@mongo:27017/")
db = client["message_db"]  # Database name
collection = db["messages"]  # Collection name


def process_message(message):
    print(f"Parsing message {message}", message)
    cleaned = {
        "text": message["text"],
        "user": message["user"],
        "tags": ["projekt"] if "projekt" in message["text"].lower() else [],
        "platform": message["platform"],
        "channel": message["channel"],
        "timestamp": message["timestamp"],
    }
    print(f"Cleaned message: {cleaned}", cleaned)

    # Insert into MongoDB
    collection.insert_one(cleaned)
    return cleaned
