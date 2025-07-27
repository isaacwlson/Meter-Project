
# Import pytest for marking async tests
import pytest

import pytest

# Test the root endpoint to ensure the API is running
@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200  # Should return HTTP 200 OK
    assert response.json()["message"].startswith("Hello world")  # Check welcome message



# Test adding and deleting an account in a single test for reliable state sharing
@pytest.mark.asyncio
async def test_add_and_delete_account(async_client):
    # Use unique values for each test run
    from uuid import uuid4
    unique_id = str(uuid4())
    payload = {
        "OAuthID": unique_id,
        "email": f"test_{unique_id}@example.com",
        "name": "Test User"
    }
    # Add account
    response = await async_client.post("/accounts/", json=payload)
    assert response.status_code == 200  # Should return HTTP 200 OK
    data = response.json()
    assert data["email"] == payload["email"]  # Email should match input
    assert "id" in data  # Response should include the new account's ID
    account_id = data["id"]

    # Test GET /accounts/{account_id}
    get_response = await async_client.get(f"/accounts/{account_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["id"] == account_id
    assert get_data["email"] == payload["email"]

    # Test GET /accounts/
    list_response = await async_client.get("/accounts/")
    assert list_response.status_code == 200
    accounts = list_response.json()
    assert any(acc["id"] == account_id for acc in accounts)

    # Test GET /health
    health_response = await async_client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "ok"

    # Delete the account
    del_response = await async_client.delete(f"/accounts/{account_id}")
    assert del_response.status_code == 200  # Should return HTTP 200 OK
    assert del_response.json()["detail"] == "Account deleted"

    # Try to delete again - should return 404 Not Found
    del_response2 = await async_client.delete(f"/accounts/{account_id}")
    assert del_response2.status_code == 404