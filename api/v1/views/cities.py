#!/usr/bin/python3
"""cities"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


# handling GET requests to retrieve a specific city in a state by its ID.
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ get all cities in a state by id method"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    cities = []
    for city in state_obj.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


# handling GET requests to retrieve city obj.
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """ get by id "method"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return (jsonify(city.to_dict()))


#  handling DELETE requests to delete a specific city by its ID.
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ delete """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


# handling POST requests to create a new city.
@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """ create city in a state """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    # retrieves JSON data from the HTTP request body.
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_city = City(name=data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    response_data = new_city.to_dict()
    return jsonify(response_data), 201


# handling PUT requests to update an existing state by its ID.
@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ Updates """
    cities = storage.all("City").values()
    city_list = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city_list == []:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    city_list[0]['name'] = request.json['name']
    for obj in cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city_list[0]), 200
