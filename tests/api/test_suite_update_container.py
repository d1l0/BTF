"""
Test Suite for Updating Containers in the API.
This suite tests the various scenarios in which a container's data can be updated via the `PUT` method.
It ensures that the API responds correctly to valid updates, partial updates, invalid fields, and other edge cases.

Test Cases:
-------------
1. **test_update_existing_container**:
    - Verifies that a container can be successfully updated with valid data.
    - The test creates a container, updates its `Hostname` and `Entrypoint`, and ensures the container is correctly updated.
    - The response is checked to ensure the updated fields match the new data, while unchanged fields remain the same.

2. **test_update_non_existent_container**:
    - Verifies that attempting to update a non-existent container (e.g., with an ID of `9999`) returns a `404 Not Found` response.
    - The response should contain an error message indicating that the container was not found.

3. **test_update_no_data**:
    - Verifies that a `PUT` request with an empty JSON body does not modify the container.
    - The test creates a container, sends an empty JSON body to update it, and ensures the container remains unchanged.

4. **test_update_partial_data**:
    - Verifies that partial updates to a container are correctly applied.
    - The test updates only the `Hostname` field of a container, leaving other fields (like `Entrypoint` and `Image`) unchanged.
    - The response is checked to ensure only the `Hostname` is updated, while other fields remain as before.

5. **test_update_invalid_fields**:
    - Verifies that attempting to update a container with invalid fields (i.e., fields not expected by the API) does not change the container's data.
    - The test attempts to update a container with invalid fields and ensures the container remains unchanged.

6. **test_update_invalid_id_format**:
    - Verifies that attempting to update a container with an invalid ID format (e.g., a string instead of a numeric ID) results in a `404 Not Found` response.
    - This ensures that the API correctly handles invalid ID formats.

7. **test_update_no_json_body**:
    - Verifies that attempting to update a container without providing a JSON body results in a `415 Unsupported Media Type` response.
    - This ensures that the API enforces the requirement for a JSON payload when updating a container.

8. **test_update_all_fields**:
    - Verifies that all fields of a container can be updated simultaneously.
    - The test creates a container and updates all fields (`Hostname`, `Entrypoint`, and `Image`). The response is checked to ensure all fields are updated accordingly.

9. **test_update_multiple_containers**:
    - Verifies that multiple containers can be updated independently of each other.
    - The test creates two containers, updates each with different data, and ensures each container is updated correctly without affecting the other.
"""

# Test updating an existing container with valid data
def test_update_existing_container(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update the container
    updated_data = {'Hostname': 'updated.hostname', 'Entrypoint': 'updated-entrypoint'}
    response = client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify the container is updated
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == updated_data['Entrypoint']
    assert updated_container['Image'] == created_container['Image']  # Ensure unchanged fields remain the same

# Test updating a non-existent container
def test_update_non_existent_container(client):
    updated_data = {'Hostname': 'new.hostname'}
    response = client.put('/orchestrator/containers/9999', json=updated_data)
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test updating a container without providing any data
def test_update_no_data(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update without providing data
    response = client.put(f'/orchestrator/containers/{created_container["id"]}', json={})
    assert response.status_code == 200
    updated_container = response.json

    # Verify the container remains unchanged
    assert updated_container == created_container

# Test updating a container with partial data
def test_update_partial_data(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update only the Hostname
    updated_data = {'Hostname': 'partial.update.hostname'}
    response = client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify updated fields and unchanged fields
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == created_container['Entrypoint']
    assert updated_container['Image'] == created_container['Image']

# Test updating a container with invalid fields
def test_update_invalid_fields(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update with invalid fields
    invalid_data = {'InvalidField': 'some value', 'AnotherInvalidField': 123}
    response = client.put(f'/orchestrator/containers/{created_container["id"]}', json=invalid_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify no changes were made
    assert updated_container == created_container

# Test updating a container with invalid ID format
def test_update_invalid_id_format(client):
    updated_data = {'Hostname': 'hostname'}
    response = client.put('/orchestrator/containers/invalid_id', json=updated_data)
    assert response.status_code == 404  # Flask default behavior for invalid route

# Test updating a container with no JSON body
def test_update_no_json_body(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Attempt to update without a JSON body
    response = client.put(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 415

# Test updating all fields of a container
def test_update_all_fields(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Update all fields
    updated_data = {
        'Hostname': 'new.hostname',
        'Entrypoint': 'new-entrypoint',
        'Image': 'new-image'
    }
    response = client.put(f'/orchestrator/containers/{created_container["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_container = response.json

    # Verify all fields are updated
    assert updated_container['Hostname'] == updated_data['Hostname']
    assert updated_container['Entrypoint'] == updated_data['Entrypoint']
    assert updated_container['Image'] == updated_data['Image']

# Test updating multiple containers independently
def test_update_multiple_containers(client, sample_data):
    # Create two containers
    container_1 = client.post('/orchestrator/containers', json=sample_data).json
    container_2 = client.post('/orchestrator/containers', json=sample_data).json

    # Update the first container
    updated_data_1 = {'Hostname': 'first.updated.hostname'}
    response = client.put(f'/orchestrator/containers/{container_1["id"]}', json=updated_data_1)
    assert response.status_code == 200
    updated_container_1 = response.json

    # Update the second container
    updated_data_2 = {'Entrypoint': 'second.updated.entrypoint'}
    response = client.put(f'/orchestrator/containers/{container_2["id"]}', json=updated_data_2)
    assert response.status_code == 200
    updated_container_2 = response.json

    # Verify updates
    assert updated_container_1['Hostname'] == updated_data_1['Hostname']
    assert updated_container_2['Entrypoint'] == updated_data_2['Entrypoint']
    assert updated_container_1['Entrypoint'] == container_1['Entrypoint']
    assert updated_container_2['Hostname'] == container_2['Hostname']
