"""Configuration file for reusable methods"""
from tools.api import app, db  # Import the Flask app and in-memory database
from datetime import datetime, timedelta
import pytest
import jwt

# Sample secret and algorithm for testing
SECRET_KEY = "dimko-qa-demchenko"
ALGORITHM = "HS256"


@pytest.fixture
def test_client():
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


@pytest.fixture
def fetch_containers(test_client):
    """
    Fixture to fetch all containers using the GET /orchestrator/containers endpoint.

    Args:
        client: The test client provided by pytest fixtures.

    Returns:
        A callable that fetches and returns all containers.
    """
    def _fetch_containers():
        response = test_client.get('/orchestrator/containers')
        assert response.status_code == 200, "Failed to fetch containers"
        return response.json

    return _fetch_containers


@pytest.fixture
def generate_test_token():
    """
    Generate a test JWT token with customizable payload.
    """
    def _generate(payload, exp_minutes=15):
        payload["exp"] = datetime.utcnow() + timedelta(minutes=exp_minutes)
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return _generate
