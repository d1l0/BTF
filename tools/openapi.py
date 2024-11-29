""""OpenAPI server for test documentation"""
import argparse
from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    title="Container Orchestrator API",
    version="0.01",
    description="API for managing containers. Use the 'Try it out' button to test the endpoints."
)

# In-memory DB
db = {}

def get_next_id():
    """
    Helper function to generate next ID
    """
    return max(db.keys(), default=0) + 1

# Define Namespace
container_ns = api.namespace("Containers", description="Container operations")

# Define Models
container_model = api.model("Container", {
    "Hostname": fields.String(required=True, description="Hostname of the container"),
    "Entrypoint": fields.String(description="Entrypoint command for the container"),
    "Image": fields.String(default="ubuntu", description="Container image"),
})

container_response = api.clone("ContainerResponse", container_model, {
    "id": fields.Integer(description="Unique ID of the container"),
})

@container_ns.route("/")
class ContainerList(Resource):
    """
    Endpoints
    """
    @container_ns.doc("list_containers")
    @container_ns.response(200, "Success", [container_response])
    @container_ns.response(400, "No containers found")
    def get(self):
        """List all containers"""
        if not db:
            return {"error": "No containers available."}, 400
        return list(db.values()), 200

    @container_ns.doc("create_container")
    @container_ns.expect(container_model, validate=True)
    @container_ns.response(201, "Created", container_response)
    @container_ns.response(400, "Invalid data")
    def post(self):
        """Create a new container"""
        data = request.json
        container_id = get_next_id()
        db[container_id] = {
            "id": container_id,
            "Hostname": data["Hostname"],
            "Entrypoint": data.get("Entrypoint", ""),
            "Image": data.get("Image", "ubuntu"),
        }
        return db[container_id], 201


@container_ns.route("/<int:container_id>")
@container_ns.param("container_id", "The unique ID of the container")
class Container(Resource):
    """
    Containers
    """
    @container_ns.doc("get_container")
    @container_ns.response(200, "Success", container_response)
    @container_ns.response(404, "Container not found")
    def get(self, container_id):
        """Retrieve a container by ID"""
        container = db.get(container_id)
        if not container:
            return {"error": "Container not found"}, 404
        return container, 200

    @container_ns.doc("update_container")
    @container_ns.expect(container_model, validate=True)
    @container_ns.response(200, "Updated", container_response)
    @container_ns.response(404, "Container not found")
    def put(self, container_id):
        """Update a container by ID"""
        data = request.json
        container = db.get(container_id)
        if not container:
            return {"error": "Container not found"}, 404
        container["Hostname"] = data.get("Hostname", container["Hostname"])
        container["Entrypoint"] = data.get("Entrypoint", container["Entrypoint"])
        container["Image"] = data.get("Image", container["Image"])
        return container, 200

    @container_ns.doc("delete_container")
    @container_ns.response(200, "Deleted")
    @container_ns.response(404, "Container not found")
    def delete(self, container_id):
        """Delete a container by ID"""
        container = db.pop(container_id, None)
        if not container:
            return {"error": "Container not found"}, 404
        return {"message": f"Container {container_id} deleted."}, 200


# Add Namespace to the API
api.add_namespace(container_ns, path="/orchestrator/containers")

if __name__ == "__main__":
    if __name__ == "__main__":
        # Use argparse to parse command-line arguments
        parser = argparse.ArgumentParser(description="Run Flask app with a custom port")
        parser.add_argument("--port", type=int, default=5050, help="Port to run the Flask app on (default: 5050)")
        parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the Flask app (default: 0.0.0.0)")

        # Parse the arguments
        args = parser.parse_args()

        # Start the Flask app with the specified port and host
        app.run(debug=True, host=args.host, port=args.port)
