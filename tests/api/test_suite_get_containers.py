"""
Test Suite for the `GET /orchestrator/containers` Endpoint

This suite includes tests for verifying the behavior of the `GET /orchestrator/containers` endpoint
under various scenarios. The tests ensure the endpoint functions as expected when the
database is empty, contains a single container, or multiple containers with varied data.

Test Cases:
1. **test_get_all_containers_empty**:
   - Verifies that the endpoint returns an appropriate error message when there are no containers in the database.

2. **test_get_all_containers_single_entry**:
   - Tests the response when the database contains exactly one container.
   - Ensures the returned container matches the one created earlier.

3. **test_get_all_containers_multiple_entries**:
   - Ensures that all containers are correctly returned when multiple containers are added.
   - Validates that each container in the database is present in the response.

4. **test_get_all_containers_structure**:
   - Confirms the structure of the response objects to ensure each container has the required keys (`id`, `Hostname`, `Entrypoint`, `Image`).
   - Validates the API's response consistency.

5. **test_get_all_containers_varied_data**:
   - Verifies that the endpoint correctly handles and returns containers with varied configurations.
   - Ensures the database maintains distinct entries and data integrity for multiple containers.

Objective:
- Validate the `GET /orchestrator/containers` endpoint's functionality, structure, and error handling across different scenarios.

Usage:
- Run this test suite with pytest to ensure the `GET /orchestrator/containers` endpoint behaves as expected.
"""
import concurrent.futures
import pytest


def test_get_all_containers_empty(test_client):
    """
    Test getting all containers when the database is empty
    """
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 400
    assert response.json == {'error': 'containers are empty'}

def test_get_all_containers_single_entry(test_client, sample_data):
    """
    Test getting all containers after adding a single container
    """
    # Add a single container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201
    created_container = response.json

    # Fetch all containers
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json

    # Verify the fetched containers list
    assert len(containers) == 1
    assert containers[0] == created_container

def test_get_all_containers_multiple_entries(test_client, sample_data):
    """
    Test getting all containers after adding multiple containers
    """
    # Add multiple containers
    response_1 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    container_1 = response_1.json

    response_2 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201
    container_2 = response_2.json

    # Fetch all containers
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json

    # Verify the fetched containers list
    assert len(containers) == 2
    assert container_1 in containers
    assert container_2 in containers

def test_get_all_containers_structure(test_client, sample_data):
    """
    Test the structure of the response when fetching all containers
    """
    # Add a container
    response = test_client.post('/orchestrator/containers', json=sample_data)
    assert response.status_code == 201

    # Fetch all containers
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json

    # Verify each container has the expected keys
    for container in containers:
        assert 'id' in container
        assert 'Hostname' in container
        assert 'Entrypoint' in container
        assert 'Image' in container

def test_get_all_containers_varied_data(test_client):
    """
    Test getting containers when there are multiple with different configurations
    """
    # Add multiple containers with different data
    container_1 = {'Hostname': 'container1', 'Entrypoint': '/bin/bash', 'Image': 'alpine'}
    container_2 = {'Hostname': 'container2', 'Entrypoint': '/start.sh', 'Image': 'nginx'}

    response_1 = test_client.post('/orchestrator/containers', json=container_1)
    assert response_1.status_code == 201
    created_1 = response_1.json

    response_2 = test_client.post('/orchestrator/containers', json=container_2)
    assert response_2.status_code == 201
    created_2 = response_2.json

    # Fetch all containers
    response = test_client.get('/orchestrator/containers')
    assert response.status_code == 200
    containers = response.json

    # Verify the fetched containers
    assert len(containers) == 2
    assert created_1 in containers
    assert created_2 in containers


@pytest.mark.xfail(reason="Known bug: [Query strings aren't implemented]", strict=True)
def test_get_all_containers_multiple_entries_with_query(test_client, sample_data):
    """
    Test getting filtered containers list. One container should return
    """
    # Add multiple containers
    response_1 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_1.status_code == 201
    container_1 = response_1.json

    response_2 = test_client.post('/orchestrator/containers', json=sample_data)
    assert response_2.status_code == 201

    # Fetch all containers with query string for only 1 container
    response = test_client.get('/orchestrator/containers?count=1')
    assert response.status_code == 200
    containers = response.json

    # Verify the fetched only 1 container
    assert len(containers) == 1
    assert container_1 in containers

@pytest.mark.xfail(reason="Known bug: [Flask client doesn't support concurrent requests]", strict=True)
def test_concurrent_get_all_containers_concurrent(test_client, fetch_containers, sample_data):
    """
    Test the GET /orchestrator/containers endpoint under concurrent requests
    """
    # Add multiple containers to the database
    for i in range(5):
        container_data = sample_data.copy()
        container_data['Hostname'] = f'container-{i}'
        response = test_client.post('/orchestrator/containers', json=container_data)
        assert response.status_code == 201

    # Verify initial state using fetch_containers
    initial_containers = fetch_containers()
    assert len(initial_containers) == 5

    # Fetch all containers concurrently
    num_concurrent_requests = 10  # Number of concurrent GET requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        # Launch multiple GET requests concurrently
        futures = [executor.submit(fetch_containers) for _ in range(num_concurrent_requests)]

        # Collect and validate results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Verify each response contains the correct number of containers
    for result in results:
        assert len(result) == 5  # Verify all 5 containers are returned
        for i in range(5):
            assert any(container['Hostname'] == f'container-{i}' for container in result)
