import os
import rdflib
import urllib.parse
from flask import Flask, Response, request, jsonify

from app.middleware.pagination import paginate

RDF_URI = os.getenv('RDF_URI', 'http://localhost:3030')
RDF_STORE = os.getenv('RDF_STORE', 'store')
RDF_USER = os.getenv('RDF_USER', 'admin')
RDF_PASSWORD = os.getenv('RDF_PASSWORD', 'pw')

RDF_URI_GET = urllib.parse.urljoin(RDF_URI, RDF_STORE, 'sparql')
# -> http://localhost:3030/store/sparql
RDF_URI_UPDATE = urllib.parse.urljoin(RDF_URI, RDF_STORE, 'update')
# -> http://localhost:3030/store/update

# Links:
# https://rdflib.github.io/sparqlwrapper/
# https://github.com/RDFLib/rdflib
# https://github.com/RDFLib/rdflib-sparqlstore
# https://github.com/RDFLib/rdflib-sparqlstore/blob/master/test/test_sparql11.py
# http://rdflib.readthedocs.io/en/stable/intro_to_sparql.html

# Setup RDF endpoint
graph = rdflib.ConjunctiveGraph('SPARQLUpdateStore')
graph.store.setCredentials(RDF_USER, RDF_PASSWORD)
graph.store.setHTTPAuth('DIGEST')
graph.open((RDF_URI_GET, RDF_URI_UPDATE))

# Setup Flask app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    response = {"status": "on"}
    return jsonify(**response)


# /courses/MAT1610
@app.route("/courses/<course_id>", methods=["GET"])
def course(course_id):
    return jsonify(data={
        "": ""
    })


@app.route("/triples", methods=["GET"])
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

    # response = []
    # for s, p, o in qres:
    #     response.append({"s": s, "p": p, "o": o})

    response = [{"s": s, "p": p, "o": o} for s, p, o in qres]

    # To JSON
    # json_string = qres.serialize(format="json")
    # print("JSON:", json_string)

    return jsonify(page=page, offset=offset, data=response)
