import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta

from shared.config import SETTINGS
from shared.storage import upload_stream, ensure_bucket, client as minio_client
from shared.db import insert_message
from shared.queue import enqueue_message_ids

SLACK_BOT_TOKEN   = SETTINGS.SLACK_BOT_TOKEN
DEFAULT_CHANNEL   = SETTINGS.SLACK_CHANNEL_ID
ATTACHMENTS_BUCKET = "slack-attachments"

def fetch_slack_streaming(channel_id: str = DEFAULT_CHANNEL,
                          subscription_id: str = DEFAULT_CHANNEL,
                          requested_by: str = "system",
                          limit: int = 100) -> list[str]:
    """
    Fetch the most recent `limit` messages from a Slack channel,
    upload any attachments to MinIO, persist each message to Mongo,
    and return the list of new message IDs.
    """
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        resp = client.conversations_history(channel=channel_id, limit=limit)
        messages = resp.get("messages", [])
    except SlackApiError as e:
        print("Slack API Error:", e.response.get("error"))
        return []

    new_ids: list[str] = []

    # Ensure bucket exists once
    ensure_bucket(ATTACHMENTS_BUCKET)

    for raw in messages:
        # Base parsed record
        parsed = {
            "platform":        "slack",
            "channel_id":      channel_id,
            "user":            raw.get("user"),
            "text":            raw.get("text", ""),
            "ts":              raw.get("ts"),
            "subscription_id": subscription_id,
            "requested_by":    requested_by,
            "fetched_at":      datetime.utcnow().isoformat(),
            "attachments":     []
        }

        # Stream each file directly into MinIO
        for f in raw.get("files", []):
            file_id   = f["id"]
            filename  = f["name"]
            url       = f.get("url_private_download", f.get("url_private"))
            headers   = {"Authorization": f"Bearer " + SLACK_BOT_TOKEN}

            r = requests.get(url, headers=headers, stream=True)
            r.raise_for_status()

            length       = int(r.headers.get("Content-Length", 0))
            content_type = r.headers.get("Content-Type", "application/octet-stream")
            object_name  = f"{subscription_id}/{file_id}_{filename}"

            upload_stream(
                bucket_name=ATTACHMENTS_BUCKET,
                object_name=object_name,
                stream=r.raw,
                length=length,
                content_type=content_type
            )

            # Generate a presigned URL for later retrieval
            public_url = minio_client.get_presigned_url(
                "GET", ATTACHMENTS_BUCKET, object_name,
                expires=timedelta(hours=1)
            )

            parsed["attachments"].append({
                "file_id":      file_id,
                "filename":     filename,
                "minio_object": object_name,
                "url":          public_url
            })

            print(f"Uploaded attachment → {public_url}")

        # Persist to Mongo and collect its ID
        msg_id = insert_message(parsed)
        new_ids.append(msg_id)

    return new_ids


def main():
    channel = os.getenv("SLACK_CHANNEL_ID", DEFAULT_CHANNEL)
    new_message_ids = fetch_slack_streaming(channel_id=channel)
    if new_message_ids:
        enqueue_message_ids(new_message_ids)
        print(f"Enqueued {len(new_message_ids)} messages:", new_message_ids)
    else:
        print("No messages fetched.")

if __name__ == "__main__":
    main()
