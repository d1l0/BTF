# Test getting a container by ID after creating it
def test_get_container_by_id_success(client, sample_data):
    # Create a container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Fetch the created container by ID
    response = client.get(f'/orchestrator/containers/{created_container["id"]}')
    assert response.status_code == 200
    fetched_container = response.json

    # Verify the fetched container matches the created container
    assert fetched_container['id'] == created_container['id']
    assert fetched_container['Hostname'] == created_container['Hostname']
    assert fetched_container['Entrypoint'] == created_container['Entrypoint']
    assert fetched_container['Image'] == created_container['Image']

# Test getting a container by an ID that does not exist
def test_get_container_by_nonexistent_id(client):
    # Attempt to fetch a container with a non-existent ID
    response = client.get('/orchestrator/containers/9999')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test getting a container by ID when no containers exist
def test_get_container_no_containers(client):
    # Attempt to fetch a container from an empty database
    response = client.get('/orchestrator/containers/1')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test getting a container with invalid ID format (e.g., string instead of integer)
def test_get_container_invalid_id_format(client):
    # Attempt to fetch a container with an invalid ID format
    response = client.get('/orchestrator/containers/invalid_id')
    assert response.status_code == 404  # Flask's default response for invalid route parameter types

# Test getting a container with a negative ID
def test_get_container_negative_id(client):
    # Attempt to fetch a container with a negative ID
    response = client.get('/orchestrator/containers/-1')
    assert response.status_code == 404
    #assert response.json == {'error': 'container not found'}

# Test getting a container after creating multiple containers
def test_get_container_among_multiple(client, sample_data):
    # Create multiple containers
    response_1 = client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    container_1 = response_1.json

    response_2 = client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    container_2 = response_2.json

    # Fetch the first container by ID
    response = client.get(f'/orchestrator/containers/{container_1["id"]}')
    assert response.status_code == 200
    fetched_container = response.json
    assert fetched_container['id'] == container_1['id']

    # Fetch the second container by ID
    response = client.get(f'/orchestrator/containers/{container_2["id"]}')
    assert response.status_code == 200
    fetched_container = response.json
    assert fetched_container['id'] == container_2['id']
