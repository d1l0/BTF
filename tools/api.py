from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory some kind of db
db = {}


# Helper function to generate next ID for simplicity
def get_next_id():
    return max(db.keys(), default=0) + 1


# CREATE: Add a new container
@app.route('/orchestrator/containers', methods=['POST'])
def create_container():
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


# READ: Get all containers
@app.route('/orchestrator/containers', methods=['GET'])
def get_containers():
    if len(db) == 0:
        return jsonify({'error': 'containers are empty'}), 400
    return jsonify(list(db.values())), 200


# READ: Get a single container by ID
@app.route('/orchestrator/containers/<int:container_id>', methods=['GET'])
def get_container(container_id):
    container = db.get(container_id)
    if not container:
        return jsonify({'error': 'container not found'}), 404
    return jsonify(container), 200


# UPDATE: Update an existing container by ID
@app.route('/orchestrator/containers/<int:container_id>', methods=['PUT'])
def update_container(container_id):
    data = request.get_json()

    container = db.get(container_id)
    if not container:
        return jsonify({'error': 'container not found'}), 404

    # Update fields if provided
    container['Hostname'] = data.get('Hostname', container['Hostname'])
    container['Entrypoint'] = data.get('Entrypoint', container['Entrypoint'])
    container['Image'] = data.get('Image', container['Image'])

    return jsonify(container), 200


# DELETE: Delete an container by ID
@app.route('/orchestrator/containers/<int:container_id>', methods=['DELETE'])
def delete_container(container_id):
    container = db.pop(container_id, None)
    if not container:
        return jsonify({'error': 'container not found'}), 404
    return jsonify({'message': f'container {container_id} deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
