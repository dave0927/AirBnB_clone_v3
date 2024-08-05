#!/usr/bin/python3
"""
    View for Place objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve all place objects"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves single Place object based on place_id"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """Creates new place"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    place = Place(name=data['name'], user_id=data['user_id'], city_id=city_id)

    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
