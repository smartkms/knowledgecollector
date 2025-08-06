from fastapi import APIRouter, Depends, HTTPException
from api.models import SubscriptionIn, SubscriptionOut
from shared.db import (
    create_subscription,
    get_subscription,
    list_subscriptions,
    update_subscription,
    delete_subscription,
)
from api.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=SubscriptionOut)
async def create_sub(data: SubscriptionIn, current_user=Depends(get_current_user)):
    # Validate payload against schema.json if you want extra layer
    sub = create_subscription(
        user_id=current_user.id,
        platform=data.platform,
        server_id=data.server_id,
        channel_id=data.channel_id,
        frequency=data.frequency,
    )
    return sub


@router.get("/{sub_id}", response_model=SubscriptionOut)
async def read_sub(sub_id: str, current_user=Depends(get_current_user)):
    sub = get_subscription(sub_id)
    if not sub or sub["user_id"] != current_user.id:
        raise HTTPException(404, "Not found")
    return sub


@router.get("/", response_model=list[SubscriptionOut])
async def list_subs(current_user=Depends(get_current_user)):
    return list_subscriptions(current_user.id)


@router.put("/{sub_id}", response_model=SubscriptionOut)
async def update_sub(
    sub_id: str, data: SubscriptionIn, current_user=Depends(get_current_user)
):
    sub = get_subscription(sub_id)
    if not sub or sub["user_id"] != current_user.id:
        raise HTTPException(404, "Not found")
    updated = update_subscription(sub_id, data.dict())
    return updated


@router.delete("/{sub_id}")
async def delete_sub(sub_id: str, current_user=Depends(get_current_user)):
    sub = get_subscription(sub_id)
    if not sub or sub["user_id"] != current_user.id:
        raise HTTPException(404, "Not found")
    delete_subscription(sub_id)
    return {"status": "deleted"}
