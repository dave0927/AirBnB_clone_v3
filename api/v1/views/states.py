#!/usr/bin/python3
"""
    View for State objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve all state objects"""
    states = storage.all("State").values()

    if states is None:
        abort(404)

    return jsonify([state.to_dict() for state in states]), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """ Retrieve single state object by state_id"""

    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    """Creates new state"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    state = State(**request.get_json())

    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
