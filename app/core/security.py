from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from jose import jwt, JWTError
from app.core.config import settings 

def create_access_token(data: Dict[str, Any], scopes: Optional[str] = None, expires_delta: Optional[timedelta] = None) -> Tuple[str, datetime]:
    to_encode = data.copy()
    if scopes:
        to_encode["scope"] = scopes
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None