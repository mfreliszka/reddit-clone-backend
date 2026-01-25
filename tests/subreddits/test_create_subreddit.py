import pytest
from syrupy.assertion import SnapshotAssertion

@pytest.mark.asyncio
async def test_create_subreddit(client, unique_username, unique_email, snapshot: SnapshotAssertion):
    # Register & Login
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })
    login_res = await client.post("/api/users/login", json={
        "username": unique_username,
        "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Subreddit
    sub_name = f"sub_{unique_username}"
    response = await client.post("/api/subreddits/", json={
        "name": sub_name,
        "description": "A test subreddit"
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sub_name
    assert "id" in data
    
    # Verify strict typing did not break logic
    assert isinstance(data["id"], int)

@pytest.mark.asyncio
async def test_create_duplicate_subreddit(client, unique_username, unique_email):
    # Register & Login
    await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })
    login_res = await client.post("/api/users/login", json={
        "username": unique_username,
        "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sub_name = f"sub_{unique_username}"
    
    # First creation
    await client.post("/api/subreddits/", json={
        "name": sub_name,
        "description": "Original"
    }, headers=headers)

    # Duplicate creation
    response = await client.post("/api/subreddits/", json={
        "name": sub_name,
        "description": "Duplicate"
    }, headers=headers)

    assert response.status_code == 400
