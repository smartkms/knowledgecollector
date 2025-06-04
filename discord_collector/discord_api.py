import httpx
from .config import DISCORD_TOKEN, CHANNEL_ID

API_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

async def fetch_messages(limit: int = 10, after_id: str | None = None) -> list[dict]:
    """
    Return the last `limit` messages from the configured channel.
    If `after_id` is provided, only messages newer than that ID will be returned.
    """
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    params: dict[str, str | int] = {"limit": limit}
    if after_id is not None:
        params["after"] = after_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()   # no await here
