"""Basic Flask API for testing"""
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
import jwt


app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ALGORITHM'] = 'HS256'

# In-memory database
db = {}


def get_next_id():
    """
    Helper function to generate next ID for simplicity
    """
    return max(db.keys(), default=0) + 1


def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'error': 'Authorization header is missing'}), 401
        try:
            token = token.split()[1]  # Expect "Bearer <token>"
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
            request.user = payload  # Attach user info to the request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """
    Decorator to enforce role-based access control
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = request.user.get('role')
            if user_role != role:
                return jsonify({'error': 'Forbidden'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route('/auth/login', methods=['POST'])
def login():
    """
    LOGIN: Authenticate a user and return a JWT token
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Mock user credentials check
    if username == 'testuser' and password == 'testpassword':
        token = jwt.encode(
            {
                'user_id': 1,
                'username': username,
                'role': 'user',
                'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            app.config['SECRET_KEY'],
            algorithm=app.config['JWT_ALGORITHM']
        )
        return jsonify({'token': token}), 200

    if username == 'admin' and password == 'adminpassword':
        token = jwt.encode(
            {
                'user_id': 2,
                'username': username,
                'role': 'admin',
                'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            app.config['SECRET_KEY'],
            algorithm=app.config['JWT_ALGORITHM']
        )
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401


# Unprotected CRUD endpoints
@app.route('/orchestrator/containers', methods=['POST'])
def create_container():
    """
    CREATE: Add a new container
    """
    data = request.get_json()

    if not data or 'Hostname' not in data:
        return jsonify({'error': 'Bad request. "Hostname" is required.'}), 400

    container_id = get_next_id()
    db[container_id] = {
        'id': container_id,
        'Hostname': data['Hostname'],
        'Entrypoint': data.get('Entrypoint', ''),
        'Image': data.get('Image', 'ubuntu')
    }

    return jsonify(db[container_id]), 201


@app.route('/orchestrator/containers', methods=['GET'])
def get_containers():
    """
    READ: Get all containers
    """
    if len(db) == 0:
        return jsonify({'error': 'containers are empty'}), 400
    return jsonify(list(db.values())), 200


@app.route('/orchestrator/containers/<int:container_id>', methods=['GET'])
def get_container(container_id):
    """
    READ: Get a single container by ID
    """
    container = db.get(container_id)
    if not container:
        return jsonify({'error': 'container not found'}), 404
    return jsonify(container), 200


@app.route('/orchestrator/containers/<int:container_id>', methods=['PUT'])
def update_container(container_id):
    """
    UPDATE: Update an existing container by ID
    """
    data = request.get_json()

    container = db.get(container_id)
    if not container:
        return jsonify({'error': 'container not found'}), 404

    # Update fields if provided
    container['Hostname'] = data.get('Hostname', container['Hostname'])
    container['Entrypoint'] = data.get('Entrypoint', container['Entrypoint'])
    container['Image'] = data.get('Image', container['Image'])

    return jsonify(container), 200


@app.route('/orchestrator/containers/<int:container_id>', methods=['DELETE'])
def delete_container(container_id):
    """
    DELETE: Delete a container by ID
    """
    container = db.pop(container_id, None)
    if not container:
        return jsonify({'error': 'container not found'}), 404
    return jsonify({'message': f'container {container_id} deleted'}), 200


# Protected endpoint examples
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    """
    Protected endpoint accessible to any authenticated user
    """
    return jsonify({'message': f'Welcome {request.user["username"]}!'}), 200


@app.route('/admin/protected', methods=['GET'])
@token_required
@role_required('admin')
def admin_protected():
    """
    Protected endpoint accessible only to admin users
    """
    return jsonify({'message': f'Admin access granted for {request.user["username"]}!'}), 200


@app.errorhandler(405)
def method_not_allowed(_):
    """
    Handle disallowed methods
    """
    return jsonify({'error': f'Method {request.method} not allowed on {request.path}'}), 405


if __name__ == '__main__':
    pass
