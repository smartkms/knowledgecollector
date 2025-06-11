from discord_collector.discord_api import list_messages
from shared.queue import enqueue_message
from shared.db import db
from datetime import datetime


def fetch_discord(server_id, channel_id, subscription_id, requested_by):
    raw_msgs = list_messages(server_id, channel_id)
    for raw in raw_msgs:
        parsed = {
            "platform": "discord",
            "server_id": server_id,
            "channel_id": channel_id,
            "author": raw.get("author", {}).get("username"),
            "content": raw.get("content"),
            "attachments": raw.get("attachments", []),
            "subscription_id": subscription_id,
            "requested_by": requested_by,
            "fetched_at": datetime.utcnow().isoformat(),
        }
        # 1) Insert into Mongo “messages” collection
        db["messages"].insert_one(parsed)
        # 2) Enqueue into message_queue for downstream
        enqueue_message(parsed)
