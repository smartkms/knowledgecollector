from dotenv import load_dotenv
import os

load_dotenv()
 
class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    MONGO_URI = os.getenv("MONGO_URI_LOCAL", "mongodb://localhost:27017/knowledge_db")
    JWT_SECRET = os.getenv("JWT_SECRET")

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    ONEDRIVE_CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID")
    ONEDRIVE_CLIENT_SECRET = os.getenv("ONEDRIVE_CLIENT_SECRET")
    ONEDRIVE_TENANT_ID = os.getenv("ONEDRIVE_TENANT_ID")
    USER_ID = os.getenv("USER_ID")

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

    MINIO_ENDPOINT   = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE     = os.getenv("MINIO_SECURE", "false").lower() == "true"

SETTINGS = Settings()
