import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# from shared.queue import enqueue_message
# from shared.db import db
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")


def fetch_slack(channel_id, subscription_id, requested_by):
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.conversations_history(channel=channel_id, limit=100)
        messages = response["messages"]
    except SlackApiError as e:
        print("Error fetching Slack messages:", e)
        return

    for raw in messages:
        parsed = {
            "platform": "slack",
            "channel_id": channel_id,
            "user": raw.get("user"),
            "text": raw.get("text"),
            "ts": raw.get("ts"),
            "subscription_id": subscription_id,
            "requested_by": requested_by,
            "fetched_at": datetime.utcnow().isoformat(),
        }
        print("Parsed message:", parsed)
        # db["messages"].insert_one(parsed)
        # enqueue_message(parsed)


def test_slack_channel(channel_id: str, message_limit: int = 5):
    """
    try:
        resp = client.conversations_join(channel=channel_id)
    except SlackApiError as e:
        print(f"❌ Failed joining channel {channel_id}: {e.response['error']}")
        return"""
    token = os.getenv("SLACK_BOT_TOKEN")

    client = WebClient(token=token)

    try:
        resp = client.conversations_history(channel=channel_id, limit=message_limit)
    except SlackApiError as e:
        print(f"❌ Slack API Error: {e.response['error']}")
        return

    messages = resp.get("messages", [])
    print(f"Showing {len(messages)} messages from channel {channel_id}:")
    for msg in messages:
        ts = msg.get("ts")
        user = msg.get("user", "unknown")
        text = msg.get("text", "")
        print(f"• [{ts}] <{user}> {text}")


if __name__ == "__main__":
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    test_slack_channel(channel_id=channel_id)
