import pytest
from jose import jwt
from app.core.config import settings
from app.core.jwt import decode_and_validate

def test_decode_valid_token():
    token = jwt.encode(
        {"sub": "123", "role": "user"},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )
    payload = decode_and_validate(token)
    assert payload["sub"] == "123"
    assert payload["role"] == "user"

def test_decode_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("invalid_token")

def test_decode_expired_token():
    from datetime import datetime, timedelta
    import time

    token = jwt.encode(
        {"sub": "123", "exp": datetime.utcnow() - timedelta(seconds=1)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )
    time.sleep(1)
    with pytest.raises(ValueError, match="Token has expired"):
        decode_and_validate(token)
