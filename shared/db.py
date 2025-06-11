from pymongo import MongoClient
from bson import ObjectId
from shared.config import SETTINGS
import isodate
from datetime import datetime

client = MongoClient(SETTINGS.MONGO_URI)
db = client.get_default_database()
subs_coll = db["subscriptions"]


def create_subscription(user_id, platform, server_id, channel_id, frequency):
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
    result = subs_coll.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}


def get_subscription(sub_id):
    doc = subs_coll.find_one({"_id": ObjectId(sub_id)})
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    return doc


def list_subscriptions(user_id):
    docs = subs_coll.find({"user_id": user_id, "active": True})
    result = []
    for doc in docs:
        doc["id"] = str(doc["_id"])
        result.append(doc)
    return result


def update_subscription(sub_id, data):
    freq_delta = isodate.parse_duration(data["frequency"])
    now = datetime.utcnow()
    next_run = now + freq_delta
    subs_coll.update_one(
        {"_id": ObjectId(sub_id)}, {"$set": {**data, "next_run": next_run}}
    )
    return get_subscription(sub_id)


def delete_subscription(sub_id):
    subs_coll.update_one({"_id": ObjectId(sub_id)}, {"$set": {"active": False}})
