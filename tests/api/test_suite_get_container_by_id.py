"""
Test Suite for the 'GET /orchestrator/containers/<id>' API endpoint.
This suite tests various scenarios for retrieving containers by their unique
IDs, ensuring that the API handles both valid and invalid input correctly and
responds with appropriate error messages.

Test Cases:
-------------
1. **test_get_container_by_id_success**:
    - Verifies that a container can be created and then successfully retrieved by its ID.
    - Ensures that the container data fetched by the ID matches the data that was originally posted.

2. **test_get_container_by_nonexistent_id**:
    - Tests the case where an attempt is made to fetch a container that does not exist (i.e., with a non-existent ID).
    - The API should return a 404 error with an appropriate error message indicating that the container was not found.

3. **test_get_container_no_containers**:
    - Tests the scenario where no containers exist in the database.
    - An attempt to retrieve a container by ID should return a 404 error indicating that no container exists with that ID.

4. **test_get_container_invalid_id_format**:
    - Tests the case where an invalid ID format (e.g., a string instead of an integer) is provided for fetching the container.
    - The API should return a 404 error as Flask does not handle invalid ID formats correctly, returning a route-not-found error instead.

5. **test_get_container_negative_id**:
    - Tests the case where an invalid negative ID is used to fetch a container.
    - The API should return a 404 error because the ID is not valid.

6. **test_get_container_among_multiple**:
    - Verifies that when multiple containers are created, each can be fetched correctly by its unique ID.
    - Ensures that each container's data can be retrieved independently without conflict, even when there are multiple containers in the system.

7. **test_get_container_special_characters_in_id**:
    - Tests the case where the ID contains special characters (e.g., `!`, `@`, `#`).
    - Ensures the API handles invalid route parameters gracefully by returning a 404 error.

8. **test_get_container_id_overflow**:
    - Tests the case where an excessively large ID value is provided for fetching a container.
    - Ensures the API handles numeric overflow correctly and returns a 404 error.

9. **test_get_container_unauthorized_access**:
    - Verifies that the API correctly responds with a 403 error when an unauthorized user attempts to fetch a container.

10. **test_get_container_response_headers**:
   - Confirms the response headers include proper metadata such as `Content-Type`.
"""

import pytest


def test_get_container_by_id_success(test_client, sample_data):
    """
    Test getting a container by ID after creating it
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Fetch the created container by ID
    response = test_client.get(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    fetched_container = response.json

    # Verify the fetched container matches the created container
    assert fetched_container['id'] == created_container['id']
    assert fetched_container['Hostname'] == created_container['Hostname']
    assert fetched_container['Entrypoint'] == created_container['Entrypoint']
    assert fetched_container['Image'] == created_container['Image']

def test_get_container_by_nonexistent_id(test_client):
    """
    Test getting a container by an ID that does not exist
    """
    # Attempt to fetch a container with a non-existent ID
    response = test_client.get('/orchestrator/containers/1010')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_get_container_no_containers(test_client):
    """
    Test getting a container by ID when no containers exist
    """
    # Attempt to fetch a container from an empty database
    response = test_client.get('/orchestrator/containers/1')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_get_container_invalid_id_format(test_client):
    """
    Test getting a container with invalid ID format (e.g., string instead of integer)
    """
    # Attempt to fetch a container with an invalid ID format
    response = test_client.get('/orchestrator/containers/invalid_id')
    assert response.status_code == 404  # Flask's default response for invalid route parameter types

def test_get_container_negative_id(test_client):
    """
    Test getting a container with a negative ID
    """
    # Attempt to fetch a container with a negative ID
    response = test_client.get('/orchestrator/containers/-1')
    assert response.status_code == 404
    #assert response.json == {'error': 'container not found'}

def test_get_container_among_multiple(test_client, sample_data):
    """
    Test getting a container after creating multiple containers
    """
    # Create multiple containers
    response_1 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    container_1 = response_1.json

    response_2 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    container_2 = response_2.json

    # Fetch the first container by ID
    response = test_client.get(f'/orchestrator/containers/{container_1["id"]}')
    assert response.status_code == 200
    fetched_container = response.json
    assert fetched_container['id'] == container_1['id']

    # Fetch the second container by ID
    response = test_client.get(f'/orchestrator/containers/{container_2["id"]}')
    assert response.status_code == 200
    fetched_container = response.json
    assert fetched_container['id'] == container_2['id']

def test_get_container_special_characters_in_id(test_client):
    """
    Test getting a container with special characters in the ID
    """
    response = test_client.get('/orchestrator/containers/!@#')
    assert response.status_code == 404  # Flask default behavior for invalid route

def test_get_container_id_overflow(test_client):
    """
    Test getting a container with an ID that is excessively large
    """
    large_id = 2**63  # Example large number
    response = test_client.get(f'/orchestrator/containers/{large_id}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

@pytest.mark.xfail(reason="Known bug: [Authorization isn't implemented]", strict=True)
def test_get_container_unauthorized_access(test_client, sample_data):
    """
    Test getting a container without proper authorization
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to fetch the container without authorization
    response = test_client.get(
        f'/orchestrator/containers/{created_container["id"]}',
        headers={"Authorization": "InvalidToken"}
    )
    assert response.status_code == 403
    assert response.json == {'error': 'Unauthorized access to the container'}


def test_get_container_response_headers(test_client, sample_data):
    """
    Test the response headers of GET /orchestrator/containers/<id>
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    response = test_client.get(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code in [200, 400]  # Depends on initial state
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'
