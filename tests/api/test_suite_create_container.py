"""
Test Suite for the 'POST /orchestrator/containers' API endpoint.
This suite tests various scenarios for creating containers, ensuring that the
API handles different types of valid and invalid input, and properly stores
the data in the simulated in-memory database.

Test Cases:
-------------
1. **test_create_container_and_verify_in_db**:
    - Verifies that when a new container is created, it is properly stored in the database and can be retrieved via GET /orchestrator/containers.

2. **test_create_container_valid_data**:
    - Ensures that creating a container with valid data results in a successfully created container with the correct attributes (id, Hostname, Entrypoint, and Image).

3. **test_create_container_missing_hostname**:
    - Tests the case where the 'Hostname' is missing in the request body. The API should return a 400 error with an appropriate error message.

4. **test_create_container_missing_entrypoint**:
    - Verifies that when the 'Entrypoint' field is missing, the container is created successfully with the default empty string as its Entrypoint.

5. **test_create_container_invalid_image**:
    - Tests creating a container with an invalid 'Image' value. In this case, the API should accept the invalid value without any validation and store it.

6. **test_create_container_empty_body**:
    - Ensures that when an empty request body is sent, the API returns a 400 error indicating that the 'Hostname' field is required.

7. **test_create_container_incomplete_data**:
    - Verifies that when the request body only contains the 'Hostname', the container is created with default values for the missing 'Entrypoint' and 'Image'.

8. **test_create_multiple_containers**:
    - Verifies that when multiple containers are created, each container has a unique 'id'.

9. **test_create_container_id_increment**:
    - Tests that the 'id' for each newly created container is incremented correctly, ensuring that the 'id' is unique and follows a consistent pattern.

10. **test_create_container_long_hostname**:
    - Verifies that the API can handle a container creation with a very long 'Hostname' (256 characters), and the container is created successfully with the long hostname.

11. **test_create_container_special_characters_in_hostname**:
    - Ensures that the API correctly handles special characters in the 'Hostname' field (e.g., '@', '#', '%') and stores the container with the exact 'Hostname' value provided.

12. **test_create_container_missing_image**:
    - Verifies that when the 'Image' field is missing, the API sets it to the default value of 'ubuntu'.
"""


def test_create_container_and_verify_in_db(client, sample_data):
    """
    Test creating a container and ensuring that data is stored properly (simulating DB state)
    """
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

def test_create_container_valid_data(client, sample_data):
    """
    Test creating a container with valid data
    """
    response = client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the correct data
    assert 'id' in created_container
    assert created_container['Hostname'] == sample_data['Hostname']
    assert created_container['Entrypoint'] == sample_data['Entrypoint']
    assert created_container['Image'] == sample_data['Image']

def test_create_container_missing_hostname(client, sample_data):
    """
    Test creating a container with missing 'Hostname'
    """
    data_missing_hostname = sample_data.copy()
    del data_missing_hostname['Hostname']

    response = client.post('/orchestrator/containers', json=data_missing_hostname)
    assert response.status_code == 400
    assert response.json == {'error': 'Bad request. "Hostname" is required.'}

def test_create_container_missing_entrypoint(client, sample_data):
    """
    Test creating a container with missing 'Entrypoint' (optional field)
    """
    data_missing_entrypoint = sample_data.copy()
    del data_missing_entrypoint['Entrypoint']

    response = client.post('/orchestrator/containers', json=data_missing_entrypoint)
    assert response.status_code == 201
    created_container = response.json

    # Verify Entrypoint is set to an empty string by default
    assert created_container['Entrypoint'] == ''

def test_create_container_invalid_image(client, sample_data):
    """
    Test creating a container with an invalid 'Image'
    """
    invalid_data = sample_data.copy()
    invalid_data['Image'] = 'invalid-image-name'

    response = client.post('/orchestrator/containers', json=invalid_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify that the invalid image is still stored correctly (no validation on image name in API)
    assert created_container['Image'] == 'invalid-image-name'

def test_create_container_empty_body(client):
    """
    Test creating a container with an empty request body
    """
    response = client.post('/orchestrator/containers', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Bad request. "Hostname" is required.'}

def test_create_container_incomplete_data(client):
    """
    Test creating a container with incomplete data (only Hostname)
    """
    incomplete_data = {'Hostname': 'test-hostname'}

    response = client.post('/orchestrator/containers', json=incomplete_data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the missing fields have default values
    assert created_container['Hostname'] == 'test-hostname'
    assert created_container['Entrypoint'] == ''
    assert created_container['Image'] == 'ubuntu'

def test_create_multiple_containers(client, sample_data):
    """
    Test creating multiple containers with unique IDs
    """
    # Create two containers
    response_1 = client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    created_container_1 = response_1.json

    response_2 = client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    created_container_2 = response_2.json

    # Verify that the containers have different IDs
    assert created_container_1['id'] != created_container_2['id']

def test_create_container_id_increment(client, sample_data):
    """
    Test creating a container and ensuring the ID is incremented correctly
    """
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

def test_create_container_long_hostname(client):
    """
    Test creating a container with a very long 'Hostname'
    """
    long_hostname = 'a' * 256  # 256 characters
    data = {'Hostname': long_hostname, 'Entrypoint': '', 'Image': 'ubuntu'}

    response = client.post('/orchestrator/containers', json=data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the long hostname
    assert created_container['Hostname'] == long_hostname

def test_create_container_special_characters_in_hostname(client):
    """
    Test creating a container with special characters in the 'Hostname'
    """
    data = {'Hostname': 'test@#%hostname!', 'Entrypoint': '', 'Image': 'ubuntu'}

    response = client.post('/orchestrator/containers', json=data)
    assert response.status_code == 201
    created_container = response.json

    # Verify the container is created with the special characters in the hostname
    assert created_container['Hostname'] == 'test@#%hostname!'


def test_create_container_missing_image(client, sample_data):
    """
    Test creating a container with missing "Image" (optional field)
    """
    data_missing_image = sample_data.copy()
    del data_missing_image['Image']

    response = client.post('/orchestrator/containers', json=data_missing_image)
    assert response.status_code == 201
    created_container = response.json

    # Verify the missing "Image" field is set to default "ubuntu"
    assert created_container['Image'] == 'ubuntu'
