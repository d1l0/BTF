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
        'name': 'Test Item',
        'description': 'A simple test item'
    }

# Test the GET /items route when no items exist
def test_get_empty_items(client):
    response = client.get('/items')
    assert response.status_code == 400
    assert response.json == {'error': 'Items are empty'}

# Test the GET /items route when some items exist
def test_get_items(client, sample_data):
    # First, create an item
    response = client.post('/items', json=sample_data)
    assert response.status_code == 201
    created_item = response.json

    # Now, test GET /items
    response = client.get('/items')
    assert response.status_code == 200
    items = response.json
    assert len(items) == 1
    assert items[0]['name'] == created_item['name']
    assert items[0]['description'] == created_item['description']

# Test the GET /items/<id> route with an existing item
def test_get_item_by_id(client, sample_data):
    # Create an item
    response = client.post('/items', json=sample_data)
    assert response.status_code == 201
    created_item = response.json

    # Fetch the created item by ID
    response = client.get(f'/items/{created_item["id"]}')
    assert response.status_code == 200
    assert response.json['id'] == created_item['id']
    assert response.json['name'] == created_item['name']
    assert response.json['description'] == created_item['description']

# Test the GET /items/<id> route with a non-existent item
def test_get_item_not_found(client):
    # Try to fetch an item that doesn't exist
    response = client.get('/items/9999')
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}
