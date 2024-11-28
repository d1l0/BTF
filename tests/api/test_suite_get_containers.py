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

# Test the GET /containers route when no containers exist
def test_get_empty_containers(client):
    response = client.get('/containers')
    assert response.status_code == 400
    assert response.json == {'error': 'containers are empty'}

# Test the GET /containers route when some containers exist
def test_get_containers(client, sample_data):
    # First, create an container
    response = client.post('/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Now, test GET /containers
    response = client.get('/containers')
    assert response.status_code == 200
    containers = response.json
    assert len(containers) == 1
    assert containers[0]['Hostname'] == created_container['Hostname']
    assert containers[0]['Entrypoint'] == created_container['Entrypoint']
    assert containers[0]['Image'] == created_container['Image']

# Test the GET /containers/<id> route with an existing container
def test_get_container_by_id(client, sample_data):
    # Create an container
    response = client.post('/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Fetch the created container by ID
    response = client.get(f'/containers/{created_container["id"]}')
    assert response.status_code == 200
    assert response.json['id'] == created_container['id']
    assert response.json['Hostname'] == created_container['Hostname']
    assert response.json['Entrypoint'] == created_container['Entrypoint']
    assert response.json['Image'] == created_container['Image']

# Test the GET /containers/<id> route with a non-existent container
def test_get_container_not_found(client):
    # Try to fetch an container that doesn't exist
    response = client.get('/containers/1010101010101010')
    assert response.status_code == 404
    assert response.json == {'error': 'container not found'}
