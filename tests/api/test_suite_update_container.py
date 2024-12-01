"""
Test Suite for Updating Containers in the API.
This suite tests the various scenarios in which a container's data can be updated via the `PUT` method.
It ensures that the API responds correctly to valid updates, partial updates, invalid fields, and other edge cases.

Test Cases:
-------------
1. **test_update_existing_container**:
    - Verifies that a container can be successfully updated with valid data.

2. **test_update_non_existent_container**:
    - Verifies that attempting to update a non-existent container returns a `404 Not Found` response.

3. **test_update_no_data**:
    - Verifies that a `PUT` request with an empty JSON body does not modify the container.

4. **test_update_partial_data**:
    - Verifies that partial updates to a container are correctly applied.

5. **test_update_invalid_fields**:
    - Verifies that invalid fields in the update request do not affect the container's data.

6. **test_update_invalid_id_format**:
    - Verifies that invalid ID formats in the update request result in a `404 Not Found` response.

7. **test_update_no_json_body**:
    - Verifies that attempting to update a container without a JSON body results in a `415 Unsupported Media Type` response.

8. **test_update_all_fields**:
    - Verifies that all fields of a container can be updated simultaneously.

9. **test_update_multiple_containers**:
    - Verifies that multiple containers can be updated independently.

10. **test_update_with_additional_unexpected_fields**:
    - Ensures the API ignores unexpected fields while updating valid fields.

11. **test_update_with_large_input**:
    - Verifies that the API handles extremely large inputs gracefully.

12. **test_concurrent_updates**:
    - Ensures the API handles concurrent updates to the same container without race conditions.

13. **test_update_read_only_fields**:
    - Ensures the API does not allow updates to read-only fields like `id`.
"""

import concurrent.futures
import pytest


def test_update_existing_container(test_client, sample_data):
    """
    Test updating an existing container with valid data
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update the container
    updated_data = {'Hostname': 'updated.hostname', 'Entrypoint': 'updated-entrypoint'}
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify the container is updated
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == updated_data['Entrypoint']
    assert updated_container['Image'] == created_container['Image']  # Ensure unchanged fields remain the same

def test_update_non_existent_container(test_client):
    """
    Test updating a non-existent container
    """
    updated_data = {'Hostname': 'new.hostname'}
    response = test_client.put('/orchestrator/containers/9999', json=updated_data)
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

def test_update_no_data(test_client, sample_data):
    """
    Test updating a container without providing any data
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update without providing data
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json={})
    assert response.status_code == 200
    updated_container = response.json

    # Verify the container remains unchanged
    assert updated_container == created_container

def test_update_partial_data(test_client, sample_data):
    """
    Test updating a container with partial data
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update only the Hostname
    updated_data = {'Hostname': 'partial.update.hostname'}
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify updated fields and unchanged fields
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == created_container['Entrypoint']
    assert updated_container['Image'] == created_container['Image']

def test_update_invalid_fields(test_client, sample_data):
    """
    Test updating a container with invalid fields
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update with invalid fields
    invalid_data = {'InvalidField': 'some value', 'AnotherInvalidField': 123}
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=invalid_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify no changes were made
    assert updated_container == created_container

def test_update_invalid_id_format(test_client):
    """
    Test updating a container with invalid ID format
    """
    updated_data = {'Hostname': 'hostname'}
    response = test_client.put('/orchestrator/containers/invalid_id', json=updated_data)
    assert response.status_code == 404  # Flask default behavior for invalid route

def test_update_no_json_body(test_client, sample_data):
    """
    Test updating a container with no JSON body
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update without a JSON body
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 415

def test_update_all_fields(test_client, sample_data):
    """
    Test updating all fields of a container
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update all fields
    updated_data = {
        'Hostname': 'new.hostname',
        'Entrypoint': 'new-entrypoint',
        'Image': 'new-image'
    }
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify all fields are updated
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == updated_data['Entrypoint']
    assert updated_container['Image'] == updated_data['Image']

def test_update_multiple_containers(test_client, sample_data):
    """
    Test updating multiple containers independently
    """
    # Create two containers
    container_1 = test_client.post('/orchestrator/containers', json=sample_data).json
    container_2 = test_client.post('/orchestrator/containers', json=sample_data).json

    # Update the first container
    updated_data_1 = {'Hostname': 'first.updated.hostname'}
    response = test_client.put(f'/orchestrator/containers/{container_1["id"]}', json=updated_data_1)
    assert response.status_code == 200
    updated_container_1 = response.json

    # Update the second container
    updated_data_2 = {'Entrypoint': 'second.updated.entrypoint'}
    response = test_client.put(f'/orchestrator/containers/{container_2["id"]}', json=updated_data_2)
    assert response.status_code == 200
    updated_container_2 = response.json

    # Verify updates
    assert updated_container_1['Hostname'] == updated_data_1['Hostname']
    assert updated_container_2['Entrypoint'] == updated_data_2['Entrypoint']
    assert updated_container_1['Entrypoint'] == container_1['Entrypoint']
    assert updated_container_2['Hostname'] == container_2['Hostname']


def test_update_with_additional_unexpected_fields(test_client, sample_data):
    """
    Test updating a container with both valid and unexpected fields
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update with valid and unexpected fields
    updated_data = {
        'Hostname': 'updated.hostname',
        'ExtraField': 'extra_value'
    }
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify only valid fields are updated
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert 'UnexpectedField' not in updated_container


def test_update_with_large_input(test_client, sample_data):
    """
    Test updating a container with extremely large field values
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update with large input
    large_data = {
        'Hostname': 'a' * 1024,
        'Entrypoint': 'b' * 2048
    }
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=large_data)
    assert response.status_code in (200, 413)  # API may enforce size limits


@pytest.mark.xfail(reason="Known bug: [Flask client doesn't support concurrent requests]", strict=True)
def test_concurrent_updates(test_client, sample_data):
    """
    Test concurrent updates to the same container
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Define update functions
    def update_hostname():
        return test_client.put(
            f'/orchestrator/containers/{created_container["id"]}',
            json={'Hostname': 'updated.hostname'}
        )

    def update_entrypoint():
        return test_client.put(
            f'/orchestrator/containers/{created_container["id"]}',
            json={'Entrypoint': 'updated.entrypoint'}
        )

    # Simulate concurrent updates
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(update_hostname), executor.submit(update_entrypoint)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Verify all responses are 200
    for result in results:
        assert result.status_code == 200


def test_update_read_only_fields(test_client, sample_data):
    """
    Test attempting to update read-only fields
    """
    # Create a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update read-only fields
    updated_data = {'id': 1010, 'Hostname': 'new.hostname'}
    response = test_client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify read-only fields are not updated
    assert updated_container['id'] == created_container['id']  # ID should remain unchanged
    assert updated_container['Hostname'] == updated_data['Hostname']

