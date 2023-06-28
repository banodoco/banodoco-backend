from datetime import datetime, timedelta
from typing import Any, Dict, Tuple
from uuid import uuid4

import jwt
from banodoco.settings import SECRET_KEY


def generate_tokens(role_id: uuid4, role_type: str) -> Tuple[str, str]:
    """Generate jwt token and refresh token for given user id and type.

    Args:
        role_id (uuid4): role uuid
        role_type (str): role type

    Returns:
        Tuple[str, str]: toke, refresh token
    """
    token_user_payload = generate_user_jwt_payload(role_id, role_type, validity_hour=24) 
    refresh_token_user_payload = generate_user_jwt_payload(role_id, role_type, validity_hour=240)
    token = jwt.encode(payload=token_user_payload, key=SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(payload=refresh_token_user_payload, key=SECRET_KEY, algorithm="HS256")
    return token, refresh_token


def generate_user_jwt_payload(role_id: uuid4, role_type: str, validity_hour: int=24) -> Dict[str, Any]:
    """Generate jwt payload_str

    Args:
        role_id (uuid4): user uuid
        role_type (str): user type
        validity_hour (int, optional): user validity_hour. Defaults to 24.

    Returns:
        Dict: jwt payload
    """
    payload = {
        'role_id' : role_id.hex,
        'role_type' : role_type,
        'iat' : datetime.utcnow(),
        'exp' : datetime.utcnow() + timedelta(hours=validity_hour)
    }
    return payload
