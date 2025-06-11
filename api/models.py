from pydantic import BaseModel, Field


class SubscriptionIn(BaseModel):
    platform: str = Field(..., regex="^(discord|slack|onedrive)$")
    server_id: str
    channel_id: str
    frequency: str  # e.g. "PT1H", "P1D"


class SubscriptionOut(SubscriptionIn):
    id: str
    user_id: int
    last_run: str | None
    active: bool
