from . import routes
from flask import request, jsonify
from app.app import * #FIX THIS IMPORT
from app.middleware.pagination import paginate

#GET /
@routes.route("/", methods=["GET"])
def root():
    response = {"status": "on"}
    return jsonify(**response)
