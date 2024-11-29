import pytest
from tools.api import app, db


# Test client fixture
@pytest.fixture
def client():
    # Set up a test client
    with app.test_client() as client:
        yield client  # This is where the test client is passed to the test

@pytest.fixture(autouse=True)  # Automatically used in every test
def reset_db():
    db.clear()

# Sample data for testing
@pytest.fixture
def sample_data():
    return {
        'Hostname': 'com.btf.containers',
        'Entrypoint': '',
        'Image': "ubuntu"
    }

# Test creating a container and ensuring that data is stored properly (simulating DB state)
def test_create_container_and_verify_in_db(client, sample_data):
    # First, create an container
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Now, test GET /orchestrator/containers
    response = client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json
    assert len(containers) == 1
    assert containers[0]['Hostname'] == created_container['Hostname']
    assert containers[0]['Entrypoint'] == created_container['Entrypoint']
    assert containers[0]['Image'] == created_container['Image']

# Test creating a container with valid data
def test_create_container_valid_data(client, sample_data):
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the correct data
    assert 'id' in created_container
    assert created_container['Hostname'] == sample_data['Hostname']
    assert created_container['Entrypoint'] == sample_data['Entrypoint']
    assert created_container['Image'] == sample_data['Image']

# Test creating a container with missing "Hostname"
def test_create_container_missing_hostname(client, sample_data):
    data_missing_hostname = sample_data.copy()
    del data_missing_hostname['Hostname']

    response = client.post('/orchestrator/containers', json=data_missing_hostname)
    assert response.status_code == 400
    assert response.json == {'error': 'Bad request. "Hostname" is required.'}

# Test creating a container with missing "Entrypoint" (optional field)
def test_create_container_missing_entrypoint(client, sample_data):
    data_missing_entrypoint = sample_data.copy()
    del data_missing_entrypoint['Entrypoint']

    response = client.post('/orchestrator/containers', json=data_missing_entrypoint)
    assert response.status_code == 201
    created_container = response.json

    # Verify Entrypoint is set to an empty string by default
    assert created_container['Entrypoint'] == ''

# Test creating a container with an invalid "Image"
def test_create_container_invalid_image(client, sample_data):
    invalid_data = sample_data.copy()
    invalid_data['Image'] = 'invalid-image-name'

    response = client.post('/orchestrator/containers', json=invalid_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify that the invalid image is still stored correctly (no validation on image name in API)
    assert created_container['Image'] == 'invalid-image-name'

# Test creating a container with an empty request body
def test_create_container_empty_body(client):
    response = client.post('/orchestrator/containers', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Bad request. "Hostname" is required.'}

# Test creating a container with incomplete data (only Hostname)
def test_create_container_incomplete_data(client):
    incomplete_data = {'Hostname': 'test-hostname'}

    response = client.post('/orchestrator/containers', json=incomplete_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the missing fields have default values
    assert created_container['Hostname'] == 'test-hostname'
    assert created_container['Entrypoint'] == ''
    assert created_container['Image'] == 'ubuntu'

# Test creating multiple containers with unique IDs
def test_create_multiple_containers(client, sample_data):
    # Create two containers
    response_1 = client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    created_container_1 = response_1.json

    response_2 = client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    created_container_2 = response_2.json

    # Verify that the containers have different IDs
    assert created_container_1['id'] != created_container_2['id']

# Test creating a container and ensuring the ID is incremented correctly
def test_create_container_id_increment(client, sample_data):
    # Create the first container
    response_1 = client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    created_container_1 = response_1.json

    # Create the second container
    response_2 = client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    created_container_2 = response_2.json

    # Ensure that the second container has an ID greater than the first one
    assert created_container_2['id'] == created_container_1['id'] + 1

# Test creating a container with a very long "Hostname"
def test_create_container_long_hostname(client):
    long_hostname = 'a' * 256  # 256 characters
    data = {'Hostname': long_hostname, 'Entrypoint': '', 'Image': 'ubuntu'}

    response = client.post('/orchestrator/containers', json=data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the long hostname
    assert created_container['Hostname'] == long_hostname

# Test creating a container with special characters in the "Hostname"
def test_create_container_special_characters_in_hostname(client):
    data = {'Hostname': 'test@#%hostname!', 'Entrypoint': '', 'Image': 'ubuntu'}

    response = client.post('/orchestrator/containers', json=data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the special characters in the hostname
    assert created_container['Hostname'] == 'test@#%hostname!'


# Test creating a container with missing "Image" (optional field)
def test_create_container_missing_image(client, sample_data):
    data_missing_image = sample_data.copy()
    del data_missing_image['Image']

    response = client.post('/orchestrator/containers', json=data_missing_image)
    assert response.status_code == 201
    created_container = response.json

    # Verify the missing "Image" field is set to default "ubuntu"
    assert created_container['Image'] == 'ubuntu'

