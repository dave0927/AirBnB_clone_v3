#!/usr/bin/python3
"""
    View for Amenity objects linked to a place,
    that handles all default RESTFul API actions
"""

from flask import abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
        Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == 'FileStorage':
        amenities = storage.all(Amenity)
        amenities = [amenity.to_dict() for amenity in amenities.values()
                     if amenity.id in place.amenity_ids]
    else:
        amenities = []

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
        Deletes a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
        Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
