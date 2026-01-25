import pytest

@pytest.mark.asyncio
async def test_get_me_authenticated(client, unique_username, unique_email):
    # Register
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })

    # Login
    login_res = await client.post("/api/users/login", json={
        "username": unique_username,
        "password": "password123"
    })
    token = login_res.json()["access_token"]

    # Get Me
    response = await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == unique_username

@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    response = await client.get("/api/users/me")
    assert response.status_code == 401 # Should be 401 as we fixed it previously
