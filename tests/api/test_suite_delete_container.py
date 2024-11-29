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
"""

# Test the DELETE /orchestrator/containers/<id> route with an existing container
def test_delete_existing_container(client, sample_data):
    # Create a container first
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the created container
    response = client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Verify the container is actually deleted
    response = client.get(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test the DELETE /orchestrator/containers/<id> route with a non-existent container
def test_delete_non_existent_container(client):
    # Attempt to delete a container that doesn't exist
    response = client.delete('/orchestrator/containers/9999')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test multiple deletions on the same container ID
def test_delete_same_container_twice(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the container the first time
    response = client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Try deleting the same container again
    response = client.delete(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test deleting all containers one by one
def test_delete_all_containers(client, sample_data):
    # Create multiple containers
    for _ in range(3):
        response = client.post('/orchestrator/containers', json=sample_data)
        assert response.status_code == 201

    # Verify all containers exist
    response = client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json
    assert len(containers) == 3

    # Delete each container
    for container in containers:
        response = client.delete(f'/orchestrator/containers/{container["id"]}')
        assert response.status_code == 200
        assert response.json == {'message': f'container {container["id"]} deleted'}

    # Verify no containers remain
    response = client.get('/orchestrator/containers')
    assert response.status_code == 400
    assert response.json == {'error': 'containers are empty'}

# Test deleting a container with invalid ID format
def test_delete_invalid_container_id(client):
    # Attempt to delete using an invalid ID format (e.g., string)
    response = client.delete('/orchestrator/containers/invalid_id')
    assert response.status_code == 404  # Flask default behavior for invalid route
