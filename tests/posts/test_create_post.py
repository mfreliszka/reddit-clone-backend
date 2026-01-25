import pytest
from syrupy.assertion import SnapshotAssertion

@pytest.mark.asyncio
async def test_create_post(client, unique_username, unique_email, snapshot: SnapshotAssertion):
    # Setup: Register, Login, Create Subreddit
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
    await client.post("/api/subreddits/", json={"name": sub_name, "description": "Test Sub"}, headers=headers)

    # Create Post
    response = await client.post(f"/api/r/{sub_name}/posts", json={
        "title": "My first post",
        "subreddit_name": sub_name,
        "content": "This is the content"
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first post"
    assert data["content"] == "This is the content"
    assert "id" in data
    assert isinstance(data["id"], int)

    # Verify retrieval
    post_id = data["id"]
    get_res = await client.get(f"/api/posts/{post_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "My first post"

@pytest.mark.asyncio
async def test_list_posts(client, unique_username, unique_email):
    # Setup
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
    
    sub_name = f"sub_{unique_username}_list"
    await client.post("/api/subreddits/", json={"name": sub_name, "description": "Test List"}, headers=headers)

    # Create 2 posts
    await client.post(f"/api/r/{sub_name}/posts", json={"title": "Post 1", "subreddit_name": sub_name}, headers=headers)
    await client.post(f"/api/r/{sub_name}/posts", json={"title": "Post 2", "subreddit_name": sub_name}, headers=headers)

    # List
    response = await client.get(f"/api/r/{sub_name}/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Post 2" # Ordered by created_at desc
    assert data[1]["title"] == "Post 1"
