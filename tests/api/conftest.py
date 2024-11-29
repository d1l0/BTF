# Configuration file for reusable methods
import pytest
from tools.api import app, db  # Import the Flask app and in-memory database

@pytest.fixture
def client():
    """Test client fixture"""
    with app.test_client() as client:
        yield client  # Provide the test client for tests

@pytest.fixture(autouse=True)
def reset_db():
    """Automatically reset the database before each test"""
    db.clear()

@pytest.fixture
def sample_data():
    """Sample data fixture for testing"""
    return {
        'Hostname': 'com.btf.containers',
        'Entrypoint': '',
        'Image': "ubuntu"
    }
