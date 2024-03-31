#!/usr/bin/python3
"""states"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """ get all """
    print ("get")
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get by id """
    print ("get id")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete """
    print ("del")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ create """
    print ("create")
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update """
    print ("update")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return (jsonify(state.to_dict()), 200)
