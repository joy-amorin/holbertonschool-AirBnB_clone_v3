#!/usr/bin/python3
"""Create a new view for City objects that
handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """Retrieves the list of all City objects"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    cities = storage.all(City).values()
    for city in cities:
        if city.state_id != state_id:
            continue
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """"Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """Creates a City:"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    post = request.get_json()
    if post is None:
        abort(400, "Not a Json")
    if "name" not in post:
        abort(400, "Missing name")
    city = City(**post)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def city_put(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    post = request.get_json()
    if post is None:
        abort(400, "Not a Json")
    for k, v in post.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
