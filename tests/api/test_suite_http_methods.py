"""
Test Suite for Method Not Allowed Errors in the API.
This suite tests the behavior of the API when HTTP methods are used incorrectly on specific endpoints.
The tests ensure that the API responds with the correct HTTP status code (405 Method Not Allowed) and an appropriate error message when an unsupported method is invoked.

Test Cases:
-------------
1. **test_method_not_allowed**:
    - Verifies that a `PATCH` request made to the `/orchestrator/containers` endpoint (which does not support the `PATCH` method) returns a 405 error.
    - The response should include an error message indicating that the `PATCH` method is not allowed on the `/orchestrator/containers` endpoint.

2. **test_method_not_allowed_id**:
    - Verifies that a `PATCH` request made to a specific container (`/orchestrator/containers/1`) also returns a 405 error.
    - The response should indicate that the `PATCH` method is not allowed for a specific container (i.e., `/orchestrator/containers/1`).

3. **test_method_allowed_list**:
    - Tests that various HTTP methods (`OPTIONS`, `PUT`, `GET`, `DELETE`, `HEAD`) are correctly handled by the API for the `/orchestrator/containers/1` endpoint.
    - The test uses the `OPTIONS` method to check which methods are allowed on the endpoint.
      The response should return a status code of 200 and the `Allow` header should include the allowed HTTP methods for the endpoint (e.g., `GET`, `DELETE`, etc.).
    - The test is parameterized for each method in the list, ensuring that all these methods are correctly validated for the endpoint.
"""

import pytest

def test_method_not_allowed(test_client):
    """
    Test that the API correctly responds with a 405 error for not-allowed HTTP methods.
    """
    # Attempt to use a PATCH method on the /orchestrator/containers endpoint
    response = test_client.patch('/orchestrator/containers')
    assert response.status_code == 405
    assert response.json == {
        'error': 'Method PATCH not allowed on /orchestrator/containers'
    }

def test_method_not_allowed_id(test_client):
    """
    Attempt to use a PATCH method on a specific container endpoint
    """
    response = test_client.patch('/orchestrator/containers/1')
    assert response.status_code == 405
    assert response.json == {
        'error': 'Method PATCH not allowed on /orchestrator/containers/1'
    }

def test_method_head(test_client, sample_data):
    """
    Attempt to use a PATCH method on a specific container endpoint
    """
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201

    response = test_client.head('/orchestrator/containers')
    assert response.status_code == 200

@pytest.mark.parametrize("method", ['OPTIONS', 'PUT', 'GET', 'DELETE', 'HEAD'])
def test_method_in_allowed_list(test_client, method):
    """
    Verify that ['OPTIONS', 'PUT', 'GET', 'DELETE', 'HEAD'] are available an endpoint route
    """
    response = test_client.options('/orchestrator/containers/1')
    assert response.status_code == 200
    assert method in response.headers['Allow']

@pytest.mark.parametrize("method", ['PUT', 'DELETE'])
def test_method_not_in_allowed_list(test_client, method):
    """
    Verify that ['PUT', 'DELETE'] aren't available an endpoint with no ['PUT', 'DELETE'] route
    """
    response = test_client.options('/orchestrator/containers')
    assert response.status_code == 200
    assert method not in response.headers['Allow']