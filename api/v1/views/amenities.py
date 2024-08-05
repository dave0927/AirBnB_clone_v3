#!/usr/bin/python3
"""
    View for Amenity objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve all amenity objects"""
    amenities = storage.all("Amenity").values()

    if amenities is None:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve single amenity object by amenity_id"""

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity object"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
    """Creates new amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    amenity = Amenity(**request.get_json())
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity"""
    amenity = storage.get("amenity", amenity_id)

    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
