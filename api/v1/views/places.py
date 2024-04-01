#!/usr/bin/python3
"""places"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


# handling GET requests to retrieve a specific place in a city by its ID.
@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """ get all place in a city by id """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    places = []
    for city in city_obj.places:
        places.append(city.to_dict())
    return jsonify(places)


# Retrieves a Place object by its ID.
@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place_id(place_id):
    """ get by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return (jsonify(place.to_dict()))


#  handling DELETE requests to delete a specific state by its ID.
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ delete """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)


# handling POST requests to create a new Place.
@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ create place"""
    # Search for city_id
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    # Handle user_id
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    # Handle name
    if 'name' not in data:
        abort(400, 'Missing name')
    # Create a new place object
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    # Return the new place object with status code 201
    return jsonify(new_place.to_dict()), 201


# handling PUT requests to update an existing place by its ID.
@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ Updates a place """
    # Get the place object with the specified ID
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # place not found

    # Get JSON data from the request
    request_json = request.get_json(silent=True)
    if not request_json:
        abort(400, 'Not a JSON')

    # Update the place object with the provided data
    for key, value in request_json.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()  # Save changes to the database

    # Return the updated place's details
    return jsonify(place.to_dict()), 200
