#!/usr/bin/python3
"""create amenities"""

from flask import Flask, jsonify, abort, request
from models import state, storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    amenit_list = []
    ameniti = storage.all(Amenity).values()
    if ameniti is None:
        abort(404)
    for amenities in ameniti:
        amenit_list.append(amenities.to_dict())
    return jsonify(amenit_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    ameniti = storage.get(Amenity, amenity_id)
    if ameniti is None:
        abort(404)
    return jsonify(ameniti.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    amenity = request.get_json(silent=True)
    if amenity is None:
        abort(400, "Not a Json")
    if "name" not in amenity:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    amenity_and_id = storage.get(Amenity, amenity_id)
    ameniti = request.get_json(silent=True)

    if amenity_and_id is None:
        abort(404)
    if ameniti is None:
        abort(400, "Not a Json")

    for key, value in ameniti.items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        setattr(amenity_and_id, key, value)
    amenity_and_id.save()
    return jsonify(amenity_and_id.to_dict()), 200
