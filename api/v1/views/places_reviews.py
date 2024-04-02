#!/usr/bin/python3
""" place review """

from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_by_place(place_id):
    """ get method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """ get by id  method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ delete  method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """ create  method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json(force=True, silent=True)
    if "user_id" not in data:
        abort(400, "Missing user_id")

    if "text" not in data:
        abort(400, "Missing text")

    user_id = data["user_id"]
    if storage.get(User, user_id) is None:
        abort(404)

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ update  method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json(force=True, silent=True)
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
