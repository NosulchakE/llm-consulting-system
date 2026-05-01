import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import engine
from app.db.base import Base

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_register_login_me_flow(client):
    # Register
    response = await client.post(
        "/api/auth/register",
        json={"email": "ivanov@email.com", "password": "test123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ivanov@email.com"
    assert data["role"] == "user"
    
    # Login
    response = await client.post(
        "/api/auth/login",
        data={"username": "ivanov@email.com", "password": "test123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Get me
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "ivanov@email.com"

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post(
        "/api/auth/register",
        json={"email": "duplicate@email.com", "password": "test123"}
    )
    response = await client.post(
        "/api/auth/register",
        json={"email": "duplicate@email.com", "password": "test123"}
    )
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/api/auth/login",
        data={"username": "nonexistent@email.com", "password": "wrong"}
    )
    assert response.status_code == 401
