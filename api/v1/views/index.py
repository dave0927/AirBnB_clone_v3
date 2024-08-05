#!/usr/bin/python3
"""
    Defines the main views of the api
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
        Returns the stats(count) of objects in each class
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats)


@app_views.route('/status', methods=['GET'])
def status():
    """
        Returns the status of the api
    """
    return jsonify({"status": "OK"})
