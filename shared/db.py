from pymongo import MongoClient
from bson import ObjectId
from shared.config import SETTINGS
import isodate
from datetime import datetime

# Initialize MongoDB client
default_db = MongoClient(SETTINGS.MONGO_URI).get_default_database()

# Subscriptions collection
default_subs = default_db["subscriptions"]

# Messages collection
default_msgs = default_db["messages"]

def create_subscription(user_id: str, platform: str, server_id: str, channel_id: str, frequency: str) -> dict:
    now = datetime.utcnow()
    freq_delta = isodate.parse_duration(frequency)
    next_run = now + freq_delta
    doc = {
        "user_id": user_id,
        "platform": platform,
        "server_id": server_id,
        "channel_id": channel_id,
        "frequency": frequency,
        "last_run": None,
        "next_run": next_run,
        "active": True,
    }
    res = default_subs.insert_one(doc)
    return {**doc, "id": str(res.inserted_id)}

def get_subscription(sub_id: str) -> dict | None:
    doc = default_subs.find_one({"_id": ObjectId(sub_id)})
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    return doc

def list_subscriptions(user_id: str) -> list[dict]:
    docs = default_subs.find({"user_id": user_id, "active": True})
    return [{**doc, "id": str(doc["_id"])} for doc in docs]

def update_subscription(sub_id: str, data: dict) -> dict:
    freq_delta = isodate.parse_duration(data["frequency"])
    next_run = datetime.utcnow() + freq_delta
    default_subs.update_one(
        {"_id": ObjectId(sub_id)},
        {"$set": {**data, "next_run": next_run}}
    )
    return get_subscription(sub_id)

def delete_subscription(sub_id: str) -> None:
    default_subs.update_one(
        {"_id": ObjectId(sub_id)},
        {"$set": {"active": False}}
    )

    # Message helpers
def insert_message(parsed: dict) -> str:
    """
    Insert a parsed message into MongoDB and return its string ID.
    """
    res = default_msgs.insert_one(parsed)
    return str(res.inserted_id)

def get_message(message_id: str) -> dict | None:
    """
    Retrieve a message document by its ID.
    """
    doc = default_msgs.find_one({"_id": ObjectId(message_id)})
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    return doc
