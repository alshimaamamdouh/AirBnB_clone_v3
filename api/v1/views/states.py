#!/usr/bin/python3
"""states"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """ get all """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get by id """
    states = storage.all("State").values()
    state_element = [state.to_dict() for state in states if state.id == state_id]
    if not state_element:
        abort(404)
    return jsonify(state_element[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ create """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    create_state = State(name=request.json['name'])
    storage.new(create_state)
    storage.save()
    states.append(create_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates """
    states = storage.all("State").values()
    state_sing = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_sing == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_sing[0]['name'] = request.json['name']
    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_sing[0]), 200
