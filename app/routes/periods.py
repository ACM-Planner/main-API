from . import routes
from flask import request, jsonify
from app.app import * #FIX THIS IMPORT
from app.middleware.pagination import paginate



# GET /periods
@routes.route("/periods", methods=["GET"])
@paginate()
def periods():
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = [
        {"year": 2016, "period": "1"},
        {"year": 2016, "period": "2"},
        {"year": 2016, "period": "TAV"},
    ]

    return jsonify(page=page, offset=offset, limit=limit, data=data)
