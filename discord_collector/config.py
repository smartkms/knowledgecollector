import os
from dotenv import load_dotenv

load_dotenv()  # look for a .env in project root

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID    = os.getenv("DISCORD_CHANNEL_ID")

if not DISCORD_TOKEN or not CHANNEL_ID:
    raise RuntimeError("You must set DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID in your .env")
