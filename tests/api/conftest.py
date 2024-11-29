import pytest
from tools.api import app, db  # Import the Flask app and in-memory database

# Test client fixture
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  # Provide the test client for tests

# Automatically reset the database before each test
@pytest.fixture(autouse=True)
def reset_db():
    db.clear()

# Sample data fixture for testing
@pytest.fixture
def sample_data():
    return {
        'Hostname': 'com.btf.containers',
        'Entrypoint': '',
        'Image': "ubuntu"
    }
