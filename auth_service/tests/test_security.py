import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token

def test_hash_password():
    password = "test123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)

def test_verify_wrong_password():
    password = "test123"
    hashed = hash_password(password)
    assert not verify_password("wrong", hashed)

def test_create_and_decode_token():
    data = {"sub": "1", "role": "user"}
    token = create_access_token(data)
    decoded = decode_token(token)
    assert decoded["sub"] == "1"
    assert decoded["role"] == "user"
    assert "exp" in decoded
    assert "iat" in decoded
