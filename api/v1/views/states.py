#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def list_states():
    """Retrieves the list of all State objects"""
    all_states = []
    states = storage.all(State).values()
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """"Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State objec"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def post_state():
    """Creates a State"""
    post = request.get_json()
    if post is None:
        abort(400, "Not a Json")
    if "name" not in post:
        abort(400, "Missing name")
    state = State(**post)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """pdates a State object"""
    state = storage.get(State, state_id)
    post = request.get_json()
    if state is None:
        abort(404)
    if post is None:
        abort(400, "Not a Json")
    for k, v in post.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
