import pytest
from syrupy.assertion import SnapshotAssertion

@pytest.mark.asyncio
async def test_login_user(client, unique_username, unique_email):
    # Register first
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })

    # Login
    response = await client.post("/api/users/login", json={
        "username": unique_username,
        "password": "password123"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["username"] == unique_username

@pytest.mark.asyncio
async def test_login_invalid_password(client, unique_username, unique_email):
    # Register first
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })

    # Login fail
    response = await client.post("/api/users/login", json={
        "username": unique_username,
        "password": "wrongpassword"
    })
    assert response.status_code == 403
