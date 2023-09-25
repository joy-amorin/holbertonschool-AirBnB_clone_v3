#!/usr/bin/python3
""" Create a new view for Place objects"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def show_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id != city_id:
            continue
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    post = request.get_json()
    if post is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in post:
        abort(400, 'Missing user_id')
    user = storage.get(User, post['user_id'])
    if user is None:
        abort(404)
    if 'name' not in post:
        abort(400, 'Missing name')
    place = Place(**post)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    put = request.get_json()
    if put is None:
        abort(400, 'Not a JSON')
    for k, v in put.items():
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
