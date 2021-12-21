import jwt
import time
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Optional


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def sign_jwt(secret: str, algo: str, user_id: int, expiration: int = 600) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + expiration * 60
    }
    token = jwt.encode(payload, secret, algorithm=algo)

    return token


def decode_jwt(secret: str, algo: str, token: str) -> Optional[int]:
    try:
        decoded_token = jwt.decode(token, secret, algorithms=[algo])

        if decoded_token["expires"] >= time.time() and decoded_token["user_id"]:
            return decoded_token["user_id"]

    except Exception:
        return None

    return None
