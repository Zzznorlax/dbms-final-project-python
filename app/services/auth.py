from fastapi import HTTPException

from app.utils.config import Settings
from app.utils.auth import decode_jwt


def verify_jwt(config: Settings, token: str) -> int:

    user_id = decode_jwt(config.JWT_SECRET, config.JWT_ALGO, token)

    if user_id is None:
        raise HTTPException(401, "jwt authentication failed")

    return user_id
