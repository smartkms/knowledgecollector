import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# from shared.queue import enqueue_message
# from shared.db import db
from datetime import datetime, timedelta
from dotenv import load_dotenv
from shared.storage import (
    client as minio_client,
)  # Assuming this is the MinIO client setup


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


def fetch_slack_streaming(
    channel_id=SLACK_CHANNEL_ID, subscription_id="0", requested_by=0
):
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        resp = client.conversations_history(channel=channel_id, limit=100)
        messages = resp.get("messages", [])
    except SlackApiError as e:
        print("Slack API Error:", e.response["error"])
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
            "attachments": [],
        }

        # Stream each file directly into MinIO
        for f in raw.get("files", []):
            file_id = f["id"]
            filename = f["name"]
            # Slack provides url_private_download for direct file content
            url = f.get("url_private_download") or f.get("url_private")
            headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}

            # Open a streaming GET
            r = requests.get(url, headers=headers, stream=True)
            r.raise_for_status()

            # Determine size and content type
            length = int(r.headers.get("Content-Length", 0))
            content_type = r.headers.get("Content-Type", "application/octet-stream")

            # Prepare bucket and object path
            bucket_name = "slack-attachments"
            object_name = f"{subscription_id}/{file_id}_{filename}"

            # Ensure bucket exists
            if not minio_client.bucket_exists(bucket_name):
                minio_client.make_bucket(bucket_name)

            # Stream upload into MinIO
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=r.raw,
                length=length,
                content_type=content_type,
            )

            # (Optionally) generate a presigned URL
            public_url = minio_client.get_presigned_url(
                "GET", bucket_name, object_name, expires=timedelta(seconds=3600)
            )

            parsed["attachments"].append(
                {
                    "file_id": file_id,
                    "filename": filename,
                    "minio_object": object_name,
                    "url": public_url,
                }
            )

        # Insert into Mongo and enqueue for downstream processing
        print(f"File available at: {public_url}")


if __name__ == "__main__":
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    fetch_slack_streaming()
