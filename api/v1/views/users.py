#!/usr/bin/python3
"""users"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


# handling GET requests to retrieve all users
@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ get all users """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# handling GET requests to retrieve a specific state by its ID.
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    """ get by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return (jsonify(user.to_dict()))


#  handling DELETE requests to delete a specific state by its ID.
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ delete """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)


# handling POST requests to create a new state.
@app_views.route('/users/', strict_slashes=False, methods=['POST'])
def create_user():
    """ create """
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(name=data['name'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


# handling PUT requests to update an existing state by its ID.
@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ Updates """
    users = storage.all("User").values()
    user_single = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_single == []:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    user_single[0]['name'] = request.json['name']
    for obj in users:
        if obj.id == user_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(user_single[0]), 200
