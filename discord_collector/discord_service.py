import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from discord_collector.discord_client import DiscordAPIClient
from shared.storage import client as minio_client
# from shared.db import db
# from shared.queue import enqueue_message

class DiscordProcessor:
    def __init__(self):
        self.api_client = DiscordAPIClient()
        self.bucket_name = "discord-attachments"
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure MinIO bucket exists"""
        if not minio_client.bucket_exists(self.bucket_name):
            minio_client.make_bucket(self.bucket_name)
    
    async def _process_attachment(self, attachment: Dict, subscription_id: str, message_id: str) -> Optional[Dict]:
        """Process a single attachment"""
        try:
            attachment_id = attachment.get("id")
            filename = attachment.get("filename", f"attachment_{attachment_id}")
            url = attachment.get("url")
            content_type = attachment.get("content_type", "application/octet-stream")
            size = attachment.get("size", 0)
            
            if not url:
                print(f"❌ No URL found for attachment {attachment_id}")
                return None

            # Download file content
            file_content = await self.api_client.download_file(url)
            
            # Create object path in MinIO
            object_name = f"{subscription_id}/{message_id}_{attachment_id}_{filename}"
            
            # Upload to MinIO
            minio_client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=io.BytesIO(file_content),
                length=len(file_content),
                content_type=content_type,
            )

            # Generate presigned URL
            public_url = minio_client.get_presigned_url(
                "GET", self.bucket_name, object_name, expires=timedelta(hours=1)
            )

            return {
                "attachment_id": attachment_id,
                "filename": filename,
                "original_url": url,
                "minio_object": object_name,
                "public_url": public_url,
                "content_type": content_type,
                "size": len(file_content)
            }

        except Exception as e:
            print(f"❌ Error processing attachment {attachment.get('id', 'unknown')}: {e}")
            return None
    
    async def _process_message(self, raw_message: Dict, server_id: str, channel_id: str, 
                              subscription_id: str, requested_by: str) -> Dict:
        """Process a single message with its attachments"""
        message_id = raw_message.get("id")
        
        # Parse basic message data
        parsed_message = {
            "platform": "discord",
            "server_id": server_id,
            "channel_id": channel_id,
            "message_id": message_id,
            "author": raw_message.get("author", {}).get("username"),
            "author_id": raw_message.get("author", {}).get("id"),
            "content": raw_message.get("content"),
            "timestamp": raw_message.get("timestamp"),
            "subscription_id": subscription_id,
            "requested_by": requested_by,
            "fetched_at": datetime.utcnow().isoformat(),
            "attachments": [],
        }

        # Process attachments
        raw_attachments = raw_message.get("attachments", [])
        if raw_attachments:
            print(f"📎 Processing {len(raw_attachments)} attachments for message {message_id}")
            
            for attachment in raw_attachments:
                processed_attachment = await self._process_attachment(
                    attachment, subscription_id, message_id
                )
                if processed_attachment:
                    parsed_message["attachments"].append(processed_attachment)
                    print(f"✅ Processed attachment: {processed_attachment['filename']}")

        return parsed_message
    
    async def fetch_and_process_messages(self, server_id: str, channel_id: str, 
                                       subscription_id: str, requested_by: str, 
                                       limit: int = 100) -> List[Dict]:
        """
        Main processing function - fetches messages and processes them with attachments
        """
        try:
            # Fetch raw messages from API
            raw_messages = await self.api_client.fetch_messages(channel_id, limit)
            print(f"📥 Fetched {len(raw_messages)} messages from Discord channel {channel_id}")
            
            processed_messages = []
            
            # Process each message
            for raw_message in raw_messages:
                processed_message = await self._process_message(
                    raw_message, server_id, channel_id, subscription_id, requested_by
                )
                processed_messages.append(processed_message)
                
                print(f"✅ Processed message {processed_message['message_id']} "
                      f"with {len(processed_message['attachments'])} attachments")
                
                # Here you would normally save to database and enqueue
                # db["messages"].insert_one(processed_message)
                # enqueue_message(processed_message)
            
            return processed_messages
            
        except Exception as e:
            print(f"❌ Error in fetch_and_process_messages: {e}")
            return []