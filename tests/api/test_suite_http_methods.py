"""
Test Suite for Method Not Allowed Errors in the API.
This suite tests the behavior of the API when HTTP methods are used incorrectly on specific endpoints.
The tests ensure that the API responds with the correct HTTP status code (405 Method Not Allowed) and an appropriate error message when an unsupported method is invoked.

T# Test Suite for Method Not Allowed Errors in the API

This suite tests the behavior of the API when HTTP methods are used incorrectly on specific endpoints.
The tests ensure that the API responds with the correct HTTP status code (`405 Method Not Allowed`) and an appropriate error message when an unsupported method is invoked.

---

### Test Cases

1. **test_method_not_allowed**:
    - Verifies that a `PATCH` request made to the `/orchestrator/containers` endpoint (which does not support the `PATCH` method) returns a 405 error.
    - The response should include an error message indicating that the `PATCH` method is not allowed on the `/orchestrator/containers` endpoint.

2. **test_method_not_allowed_id**:
    - Verifies that a `PATCH` request made to a specific container (`/orchestrator/containers/1`) also returns a 405 error.
    - The response should indicate that the `PATCH` method is not allowed for a specific container (i.e., `/orchestrator/containers/1`).

3. **test_method_head**:
    - Ensures that the `HEAD` method is allowed on the `/orchestrator/containers` endpoint.
    - Validates that no response body is returned when the `HEAD` method is used.

4. **test_method_in_allowed_list**:
    - Verifies that the HTTP methods `OPTIONS`, `PUT`, `GET`, `DELETE`, and `HEAD` are supported on the `/orchestrator/containers/1` endpoint.
    - Uses the `OPTIONS` method to check the `Allow` header for the list of supported methods.

5. **test_method_not_in_allowed_list**:
    - Verifies that the HTTP methods `PUT` and `DELETE` are not available on the `/orchestrator/containers` endpoint.
    - Uses the `OPTIONS` method to check the `Allow` header and ensure these methods are not listed.

6. **test_method_put_not_in_allowed_list**:
    - Verifies that the `PUT` method is not supported on the `/orchestrator/containers` endpoint.
    - Ensures a `405 Method Not Allowed` error is returned.

7. **test_method_delete_not_in_allowed_list**:
    - Verifies that the `DELETE` method is not supported on the `/orchestrator/containers` endpoint.
    - Ensures a `405 Method Not Allowed` error is returned.

8. **test_method_options_supported**:
    - Ensures that the `OPTIONS` method is supported on the `/orchestrator/containers` endpoint.
    - Validates that the response contains the `Allow` header listing the supported methods.

9. **test_method_options_supported**:
    - Ensures that the `OPTIONS` method is supported on the `/orchestrator/containers/id` endpoint.
    - Validates that the response contains the `Allow` header listing the supported methods.

10. **test_method_post_not_allowed_on_specific_container**:
    - Verifies that the `POST` method is not supported on a specific container (`/orchestrator/containers/1`) endpoint.
    - Ensures a `405 Method Not Allowed` error is returned with an appropriate error message.

---
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
    Attempt to use a HEAD method on a specific container endpoint
    """
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201

    response = test_client.head('/orchestrator/containers')
    assert response.status_code == 200

    # Validate that no body is returned
    assert response.data == b''

def test_method_head_id(test_client, sample_data):
    """
    Attempt to use a HEAD method on a specific container endpoint
    """
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201

    response = test_client.head('/orchestrator/containers/1')
    assert response.status_code == 200

    # Validate that no body is returned
    assert response.data == b''

def test_method_options_supported_conteiners(test_client):
    """
    Verify that the OPTIONS method is supported on the /orchestrator/containers endpoint
    """
    response = test_client.options('/orchestrator/containers')
    assert response.status_code == 200

def test_method_options_supported_conteiners_id(test_client, sample_data):
    """
    Verify that the OPTIONS method is supported on the /orchestrator/containers/id endpoint
    """
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201

    response = test_client.options('/orchestrator/containers/1')
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

@pytest.mark.parametrize("method", ['POST'])
def test_method_not_in_allowed_list_id(test_client, method):
    """
    Verify that 'POST' aren't available an endpoint with no ['POST'] route
    """
    response = test_client.options('/orchestrator/containers/1')
    assert response.status_code == 200
    assert method not in response.headers['Allow']

def test_method_put_not_in_allowed_list(test_client):
    """
    Verify that 'PUT' aren't allowed an endpoint with no 'PUT' route
    """
    response = test_client.put('/orchestrator/containers')
    assert response.status_code == 405
    assert response.json == {
        'error': 'Method PUT not allowed on /orchestrator/containers'
    }

def test_method_delete_not_in_allowed_list(test_client):
    """
    Verify that 'DELETE' aren't allowed an endpoint with no 'DELETE' route
    """
    response = test_client.delete('/orchestrator/containers')
    assert response.status_code == 405
    assert response.json == {
        'error': 'Method DELETE not allowed on /orchestrator/containers'
    }

def test_method_post_not_allowed_on_specific_container(test_client):
    """
    Verify that POST is not allowed on /orchestrator/containers/1 endpoint
    """
    response = test_client.post('/orchestrator/containers/1')
    assert response.status_code == 405
    assert response.json == {
        'error': 'Method POST not allowed on /orchestrator/containers/1'
    }
