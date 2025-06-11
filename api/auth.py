from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from shared.db import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = None  # loaded from .env in shared/config.py


def setup_auth(app):
    global JWT_SECRET
    from shared.config import SETTINGS

    JWT_SECRET = SETTINGS.JWT_SECRET


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = get_user_by_id(payload["sub"])
        return user
    except Exception:
        raise HTTPException(401, "Invalid authentication")
