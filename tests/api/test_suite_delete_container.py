import pytest
from tools.api import app

# Test client fixture
@pytest.fixture
def client():
    # Set up a test client
    with app.test_client() as client:
        yield client  # This is where the test client is passed to the test

# Sample data for testing
@pytest.fixture
def sample_data():
    return {
        'Hostname': 'com.btf.containers',
        'Entrypoint': '',
        'Image': "ubuntu"
    }
# Test the DELETE /containers/<id> route with an existing container
def test_delete_existing_container(client, sample_data):
    # Create a container first
    response = client.post('/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the created container
    response = client.delete(f'/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Verify the container is actually deleted
    response = client.get(f'/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test the DELETE /containers/<id> route with a non-existent container
def test_delete_non_existent_container(client):
    # Attempt to delete a container that doesn't exist
    response = client.delete('/containers/9999')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test multiple deletions on the same container ID
def test_delete_same_container_twice(client, sample_data):
    # Create a container
    response = client.post('/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Delete the container the first time
    response = client.delete(f'/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json == {'message': f'container {created_container["id"]} deleted'}

    # Try deleting the same container again
    response = client.delete(f'/containers/{created_container["id"]}')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}

# Test deleting all containers one by one
def test_delete_all_containers(client, sample_data):
    # Create multiple containers
    for i in range(3):
        response = client.post('/containers', json=sample_data)
        assert response.status_code == 201

    # Verify all containers exist
    response = client.get('/containers')
    assert response.status_code == 200
    containers = response.json
    assert len(containers) == 3

    # Delete each container
    for container in containers:
        response = client.delete(f'/containers/{container["id"]}')
        assert response.status_code == 200
        assert response.json == {'message': f'container {container["id"]} deleted'}

    # Verify no containers remain
    response = client.get('/containers')
    assert response.status_code == 400
    assert response.json == {'error': 'containers are empty'}

# Test deleting a container with invalid ID format
def test_delete_invalid_container_id(client):
    # Attempt to delete using an invalid ID format (e.g., string)
    response = client.delete('/containers/invalid_id')
    assert response.status_code == 404  # Flask default behavior for invalid route
