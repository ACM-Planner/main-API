from . import routes
from flask import request, jsonify
from app.app import * #FIX THIS IMPORT 
from app.middleware.pagination import paginate

#GET /triples
@routes.route("/triples", methods=["GET"])
@paginate()
def resource_names():
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    # See qres (Result) documentation:
    # http://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.query.Result
    qres = graph.query("""
        SELECT * WHERE {{ ?s ?p ?o. }} LIMIT {limit} OFFSET {offset}
    """.format(limit=limit, offset=offset))

    # data = []
    # for s, p, o in qres:
    #     data.append({"s": s, "p": p, "o": o})

    data = [{"s": s, "p": p, "o": o} for s, p, o in qres]

    # To JSON
    # json_string = qres.serialize(format="json")
    # print("JSON:", json_string)

    return jsonify(page=page, offset=offset, limit=limit, data=data)
