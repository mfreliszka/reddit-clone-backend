import pytest

@pytest.mark.asyncio
async def test_get_user_profile(client, unique_username, unique_email):
    # Register
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })

    # Get Profile
    response = await client.get(f"/api/users/{unique_username}")
    assert response.status_code == 200
    assert response.json()["username"] == unique_username

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/api/users/nonexistent_user")
    assert response.status_code == 404
