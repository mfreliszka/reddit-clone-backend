import pytest
from syrupy.assertion import SnapshotAssertion

@pytest.mark.asyncio
async def test_register_user(client, unique_username, unique_email, snapshot: SnapshotAssertion):
    response = await client.post("/api/users/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "password123"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == unique_username
    assert "id" in data
    assert "password" not in data
    
    # Snapshot testing structure (excluding dynamic fields)
    assert {k: v for k, v in data.items() if k not in ["id", "username", "email"]} == snapshot
