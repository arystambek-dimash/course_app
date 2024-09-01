import jwt
from datetime import datetime, timezone
from typing import Optional

from src.db.schemas.tokens import Payload
from src.core.config import settings


def create_access_token(data: Payload) -> str:
    to_encode = data.dict().copy()
    expire = datetime.now(timezone.utc) + data.exp
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_ACCESS_TOKEN, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Payload]:
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_TOKEN, algorithms=["HS256"])
        return Payload(_id=payload['id'], **payload)
    except jwt.ExpiredSignatureError:
        print("Access token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid access token: {str(e)}")
        return None


def create_refresh_token(data: Payload) -> str:
    to_encode = data.dict().copy()
    expire = datetime.now(timezone.utc) + data.exp
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_TOKEN, algorithm="HS256")
    return encoded_jwt


def decode_refresh_token(token: str) -> Optional[Payload]:
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_TOKEN, algorithms=["HS256"])
        return Payload(_id=payload['id'], **payload)
    except jwt.ExpiredSignatureError:
        print("Refresh token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid refresh token: {str(e)}")
        return None
