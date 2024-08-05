#!/usr/bin/python3
"""
    View for user objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve all user objects"""
    users = storage.all("User").values()

    if users is None:
        abort(404)

    return jsonify([user.to_dict() for user in users]), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """ Retrieve single user object by user_id"""

    user = storage.get("User", user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user object"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def add_user():
    """Creates new user"""
    if not request.json:
        abort(400, "Not a JSON")

    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")

    user = User(**request.get_json())

    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates user"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
