from flask import Flask, Response, request, jsonify

# Links:
# https://rdflib.github.io/sparqlwrapper/
# https://github.com/RDFLib/rdflib
# https://github.com/RDFLib/rdflib-sparqlstore
# https://github.com/RDFLib/rdflib-sparqlstore/blob/master/test/test_sparql11.py
# http://rdflib.readthedocs.io/en/stable/intro_to_sparql.html

# from SPARQLWrapper import SPARQLWrapper, JSON
#
# RDF_ENDPOINT = "http://192.168.99.100:3030/test/query"
#
# sparql = SPARQLWrapper(RDF_ENDPOINT)
# sparql.setReturnFormat(JSON)
#
# # add a default graph, though that can also be part of the query string
# # sparql.addDefaultGraph("http://www.example.com/data.rdf")
#
# queryString = "SELECT * WHERE { ?s ?p ?o. }"
# sparql.setQuery(queryString)
#
# try:
#     result = sparql.query().convert()
#     print(result)
# except Exception as e:
#     print(e)

# -----------------------

# from rdflib import ConjunctiveGraph, URIRef
#
# graphuri = URIRef('urn:default')
#
# graph = ConjunctiveGraph('SPARQLUpdateStore')
# root = "http://192.168.99.100:3030/test/"
# graph.open((root + "query", root + "update"))
#
# g = graph.get_context(graphuri)

# g = rdflib.ConjunctiveGraph('SPARQLUpdateStore')

# -----------------------

import rdflib

graph = rdflib.ConjunctiveGraph('SPARQLStore')
graph.open("http://192.168.99.100:3030/test/sparql")

qres = graph.query("""
    SELECT * WHERE { ?s ?p ?o. }
""")

# See qres (Result) documentation:
# http://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.query.Result

# As triples
for s, p, o in qres:
    print('----------')
    print('s:', s)
    print('p:', p)
    print('o:', o)

# To JSON
json_string = qres.serialize(format='json')
print('JSON:', json_string)


app = Flask(__name__)

# In-memory data store
names = [
    'Patricio López',
]


@app.route("/")
def hello():
    response = {"status": "on"}
    return jsonify(**response)


@app.route('/names', methods=['GET', 'POST'])
def resource_names():
    if request.method == 'GET':
        # Return current values
        return jsonify(names=names)

    elif request.method == 'POST':
        # Obtain JSON from request body
        content = request.get_json(silent=True)  # Do not throw exception

        if 'name' in content:
            names.append(content['name'])
            # 201 CREATED | https://httpstatuses.com/201
            return jsonify(name=content['name']), 201
        else:
            # 406 NOT ACCEPTABLE | https://httpstatuses.com/406
            return Response(status=406)

    else:
        # 501 NOT IMPLEMENTED | https://httpstatuses.com/501
        return Response(status=501)
