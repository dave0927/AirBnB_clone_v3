#!/usr/bin/python3
"""
    View for Review objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves reviews of a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route("/reviews/<review_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review by review_id"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def add_review(place_id):
    """Creates a Review"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user_id = data["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    data["place_id"] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
