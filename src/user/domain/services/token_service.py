import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict

from jose import JWTError, jwt

from core.config import settings

log = logging.getLogger(__name__)


class TokenService:
    """Domain service for JWT token operations"""

    SECRET_KEY = settings.auth.SECRET_KEY
    ALGORITHM = settings.auth.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def create_access_token(cls, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        log.info(f"Token expiration (UTC): {expire}")
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        # Explicitly encode to bytes and then decode to string to ensure clean string representation
        clean_jwt_string = str(encoded_jwt).encode("utf-8").decode("utf-8")
        return clean_jwt_string

    @classmethod
    def decode_access_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate a JWT token"""
        try:
            payload: Dict[str, Any] = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError as e:
            log.error(f"JWTError during token decoding: {e}")
            return None
