# discord_api.py - Pure API client
import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

class DiscordAPIClient:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.base_url = "https://discord.com/api/v10"
        self.headers = {"Authorization": f"Bot {self.token}"}
    
    async def fetch_messages(self, channel_id: str, limit: int = 100) -> list:
        """Fetch messages from a Discord channel"""
        url = f"{self.base_url}/channels/{channel_id}/messages"
        params = {"limit": min(limit, 100)}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def download_file(self, url: str) -> bytes:
        """Download file content from Discord CDN"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content