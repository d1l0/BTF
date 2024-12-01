"""
Test Suite for the 'DELETE /orchestrator/containers/<id>' API endpoint.
This suite tests various scenarios for deleting containers, ensuring that the
API handles different types of valid and invalid input, and responds correctly
to various deletion scenarios.

Test Cases:
-------------
1. **test_delete_existing_container**:
    - Verifies that a container can be created and then successfully deleted.
    - Ensures that after deletion, the container is no longer retrievable via the GET API endpoint.

2. **test_delete_non_existent_container**:
    - Tests the case where an attempt is made to delete a container that doesn't exist.
    - The API should return a 404 error with an appropriate error message.

3. **test_delete_same_container_twice**:
    - Verifies that when a container is deleted, subsequent attempts to delete the same container return a 404 error.
    - Ensures that the system correctly handles multiple delete requests on the same container.

4. **test_delete_all_containers**:
    - Ensures that multiple containers can be created and deleted in sequence.
    - Verifies that after all containers are deleted, no containers remain in the system and the API returns the correct empty state.

5. **test_delete_invalid_container_id**:
    - Tests the scenario where an invalid container ID format (e.g., a string instead of an integer) is provided for deletion.
    - The API should return a 404 error, as Flask does not route such requests to the proper endpoint.

6. **test_delete_unauthorized**:
    - Verifies that the API correctly responds with a 403 error when an unauthorized user attempts to delete a container.

Additional TC's (Not Implemented): #TODO

7. **test_delete_with_dependencies**:
    - Tests deleting a container that has active dependencies, ensuring that the API either prevents deletion or handles it properly.

8. **test_bulk_delete_containers**:
    - Verifies that multiple containers can be deleted in a single bulk deletion request.
    - Ensures proper handling of both valid and invalid container IDs in the bulk request.
"""
import pytest


def test_delete_existing_container(test_client, sample_data):
    """
    Test the DELETE /orchestrator/containers/<id> route with an existing container
    """
    # Create a container first
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the created container
    response = test_client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Verify the container is actually deleted
    response = test_client.get(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_delete_non_existent_container(test_client):
    """
    Test the DELETE /orchestrator/containers/<id> route with a non-existent container
    """
    # Attempt to delete a container that doesn't exist
    response = test_client.delete('/orchestrator/containers/9999')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_delete_same_container_twice(test_client, sample_data):
    """
    Test multiple deletions on the same container ID
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the container the first time
    response = test_client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Try deleting the same container again
    response = test_client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_delete_all_containers(test_client, sample_data):
    """
    Test deleting all containers one by one
    """
    # Create multiple containers
    for _ in range(3):
        response = test_client.post('/orchestrator/containers', json=sample_data)
        assert response.status_code == 201

    # Verify all containers exist
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json
    assert len(containers) == 3

    # Delete each container
    for container in containers:
        response = test_client.delete(f'/orchestrator/containers/{container["id"]}')
        assert response.status_code == 200
        assert response.json == {'message': f'container {container["id"]} deleted'}

    # Verify no containers remain
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 400
    assert response.json == {'error': 'containers are empty'}

def test_delete_invalid_container_id(test_client):
    """
    Test deleting a container with invalid ID format
    """
    # Attempt to delete using an invalid ID format (e.g., string)
    response = test_client.delete('/orchestrator/containers/invalid_id')
    assert response.status_code == 404  # Flask default behavior for invalid route

@pytest.mark.xfail(reason="Known bug: [Authorization isn't implemented]", strict=True)
def test_delete_unauthorized(test_client, sample_data):
    """
    Test attempting to delete a container without proper authorization
    """
    # Assuming some form of authorization is required (e.g., API key, token)
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to delete the container without authorization
    response = test_client.delete(
        f'/orchestrator/containers/{created_container["id"]}',
        headers={"Authorization": "InvalidToken"}
    )
    assert response.status_code == 403
    assert response.json == {'error': 'Unauthorized to delete the container'}
