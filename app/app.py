import os
import rdflib
import urllib.parse
from flask import Flask, Response, request, jsonify

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


@app.route("/")
def root():
    response = {"status": "on"}
    return jsonify(**response)


@app.route('/triples')
def resource_names():
    if request.method != 'GET':
        # 501 NOT IMPLEMENTED | https://httpstatuses.com/501
        return Response(status=501)

    # See qres (Result) documentation:
    # http://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.query.Result
    qres = graph.query("""
        SELECT * WHERE { ?s ?p ?o. }
    """)

    response = []

    # As triples
    for s, p, o in qres:
        response.append({'s': s, 'p': p, 'o': o})

    # To JSON
    # json_string = qres.serialize(format='json')
    # print('JSON:', json_string)

    return jsonify(triples=response)
