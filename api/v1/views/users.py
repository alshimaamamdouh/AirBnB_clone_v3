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
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


# handling PUT requests to update an existing state by its ID.
@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ Updates a user's name """
    # Get the user object with the specified ID
    user = storage.get(User, user_id)
    if not user:
        abort(404)  # User not found

    # Get JSON data from the request
    request_json = request.get_json(silent=True)
    if not request_json:
        abort(400, 'Not a JSON')

    # Get the new name from the JSON data
    new_name = request_json.get('name')
    if not new_name:
        abort(400, 'Missing name')

    # Update the user's name
    user.name = new_name
    storage.save()  # Save changes to the database

    # Return the updated user's details
    return jsonify(user.to_dict()), 200

    # users = storage.all(User).values()
    # user_dict = [obj.to_dict() for obj in users if obj.id == user_id]
    # if not user_dict:
    #     abort(404)
    #  # Get JSON data from the request
    # request_json = request.get_json(silent=True)
    # if not request_json:
    #     abort(400, 'Not a JSON')
    #  # Get the new name from the JSON data
    # new_name = request_json['name']
    # user_dict[0]['name'] = new_name
    # for obj in users:
    #     if obj.id == user_id:
    #         obj.name = new_name
    # storage.save()
    # return jsonify(user_dict[0]), 200
