import pytest

@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello world")

@pytest.mark.asyncio
async def test_add_account(async_client):
    payload = {
        "OAuthID": "abc123",
        "email": "test@example.com",
        "name": "Test User"
    }
    response = await async_client.post("/accounts/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    # Save the account ID for deletion
    global created_account_id
    created_account_id = data["id"]

@pytest.mark.asyncio
async def test_delete_account(async_client):
    response = await async_client.delete(f"/accounts/{created_account_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Account deleted"

    # Try to delete again - should 404
    response = await async_client.delete(f"/accounts/{created_account_id}")
    assert response.status_code == 404