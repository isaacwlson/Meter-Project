
# Import pytest for marking async tests
import pytest

# Test the root endpoint to ensure the API is running
@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200  # Should return HTTP 200 OK
    assert response.json()["message"].startswith("Hello world")  # Check welcome message

# Test adding a new account via the /accounts/ endpoint
# Note: Uses a global variable to share the created account ID with the delete test
# In production, prefer using a fixture to share state between tests
@pytest.mark.asyncio
async def test_add_account(async_client):
    payload = {
        "OAuthID": "abc123",
        "email": "test@example.com",
        "name": "Test User"
    }
    response = await async_client.post("/accounts/", json=payload)
    assert response.status_code == 200  # Should return HTTP 200 OK
    data = response.json()
    assert data["email"] == payload["email"]  # Email should match input
    assert "id" in data  # Response should include the new account's ID

    # Save the account ID for deletion in the next test
    global created_account_id
    created_account_id = data["id"]

# Test deleting the account created in the previous test
@pytest.mark.asyncio
async def test_delete_account(async_client):
    # Delete the account by ID
    response = await async_client.delete(f"/accounts/{created_account_id}")
    assert response.status_code == 200  # Should return HTTP 200 OK
    assert response.json()["detail"] == "Account deleted"

    # Try to delete again - should return 404 Not Found
    response = await async_client.delete(f"/accounts/{created_account_id}")
    assert response.status_code == 404