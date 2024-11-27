from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory some kind of db
db = {}


# Helper function to generate next ID for simplicity
def get_next_id():
    return max(db.keys(), default=0) + 1


# CREATE: Add a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Bad request. "name" is required.'}), 400

    item_id = get_next_id()
    db[item_id] = {
        'id': item_id,
        'name': data['name'],
        'description': data.get('description', '')
    }

    return jsonify(db[item_id]), 201


# READ: Get all items
@app.route('/items', methods=['GET'])
def get_items():
    if len(db) == 0:
        return jsonify({'error': 'Items are empty'}), 400
    return jsonify(list(db.values())), 200


# READ: Get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item), 200


# UPDATE: Update an existing item by ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()

    item = db.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Update fields if provided
    item['name'] = data.get('name', item['name'])
    item['description'] = data.get('description', item['description'])

    return jsonify(item), 200


# DELETE: Delete an item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.pop(item_id, None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'message': f'Item {item_id} deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
