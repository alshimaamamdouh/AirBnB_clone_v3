#!/usr/bin/python3
"""amenities"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


# handling GET requests to retrieve all amenities
@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ get all method"""
    amenities = storage.all(Amenity).values()
    return jsonify([amen.to_dict() for amen in amenities])


# handling GET requests to retrieve a specific state by its ID.
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_id(amenity_id):
    """ get by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return (jsonify(amenity.to_dict()))


#  handling DELETE requests to delete a specific state by its ID.
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete method """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


# handling POST requests to create a new state.
@app_views.route('/amenities/', strict_slashes=False, methods=['POST'])
def create_amenity():
    """ create """
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=data['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


# handling PUT requests to update an existing state by its ID.
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def updates_amenity(amenity_id):
    """ Updates """
    amenities = storage.all("Amenity").values()
    state_sing = [obj.to_dict() for obj in amenities if obj.id == amenity_id]
    if state_sing == []:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    state_sing[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_sing[0]), 200
