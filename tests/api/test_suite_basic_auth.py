"""
Test Suite for Flask API with JWT-based Authentication and Authorization.

This suite tests various scenarios to ensure that the Flask API correctly handles
JWT-based authentication and authorization. It validates token generation,
protected endpoint access, and error handling for invalid or expired tokens.

Test Cases:
-------------
1. **test_generate_token**:
    - Verifies that the `/auth/login` endpoint returns a valid JWT token for correct credentials.

2. **test_access_protected_endpoint_with_valid_token**:
    - Verifies that a valid JWT token allows access to a protected endpoint.

3. **test_access_protected_endpoint_without_token**:
    - Verifies that accessing a protected endpoint without a token returns a `401 Unauthorized` error.

4. **test_access_protected_endpoint_with_invalid_token**:
    - Verifies that accessing a protected endpoint with an invalid token returns a `401 Unauthorized` error.

5. **test_access_protected_endpoint_with_expired_token**:
    - Verifies that accessing a protected endpoint with an expired token returns a `401 Unauthorized` error.

6. **test_access_protected_endpoint_with_invalid_claims**:
    - Verifies that accessing a protected endpoint with a token containing invalid claims returns a `403 Forbidden` error.

7. **test_access_protected_endpoint_with_insufficient_permissions**:
    - Verifies that a valid token with insufficient permissions returns a `403 Forbidden` error.

#TODO add some admin role testing, etc.
"""
import pytest


def test_generate_token(test_client):
    """
    Test that the login endpoint generates a valid JWT token.
    """
    # Mock login credentials
    credentials = {"username": "testuser", "password": "testpassword"}
    response = test_client.post('/auth/login', json=credentials)
    assert response.status_code == 200
    assert "token" in response.json


@pytest.mark.xfail(reason="To Investigate: [Review token creation method]", strict=True)
def test_access_protected_endpoint_with_valid_token(test_client, generate_test_token):
    """
    Test accessing a protected endpoint with a valid token.
    """
    token = generate_test_token({"user_id": 1, "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get('/protected', headers=headers)
    assert response.status_code == 200


def test_access_protected_endpoint_without_token(test_client):
    """
    Test accessing a protected endpoint without a token.
    """
    response = test_client.get('/protected')
    assert response.status_code == 401
    assert response.json == {"error": "Authorization header is missing"}


def test_access_protected_endpoint_with_invalid_token(test_client):
    """
    Test accessing a protected endpoint with an invalid token.
    """
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = test_client.get('/protected', headers=headers)
    assert response.status_code == 401
    assert response.json == {"error": "Invalid or expired token"}


def test_access_protected_endpoint_with_expired_token(test_client, generate_test_token):
    """
    Test accessing a protected endpoint with an expired token.
    """
    expired_token = generate_test_token({"user_id": 1, "role": "user"}, exp_minutes=-1)
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = test_client.get('/protected', headers=headers)
    assert response.status_code == 401
    assert response.json == {"error": "Invalid or expired token"}


@pytest.mark.xfail(reason="To Investigate: [Review token creation method]", strict=True)
def test_access_protected_endpoint_with_invalid_claims(test_client, generate_test_token):
    """
    Test accessing a protected endpoint with invalid claims in the token.
    """
    token = generate_test_token({"user_id": 1, "role": "invalid_role"})
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get('/protected', headers=headers)
    assert response.status_code == 403
    assert response.json == {"error": "Forbidden"}


@pytest.mark.xfail(reason="To Investigate: [Review token creation method]", strict=True)
def test_access_protected_endpoint_with_insufficient_permissions(test_client, generate_test_token):
    """
    Test accessing a protected endpoint with insufficient permissions.
    """
    token = generate_test_token({"user_id": 1, "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get('/admin/protected', headers=headers)
    assert response.status_code == 403
    assert response.json == {"error": "Forbidden"}
