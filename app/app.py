import os
import rdflib
import urllib.parse
import re
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from app.routes import *


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
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(routes)
CORS(app)


#Return parsed data of the query in a dictionary
#Doesn't work when using SELECT *
def make_query(query):

    #makes the query
    qres = graph.query(query)

    #parse into a dictionary
    for i in qres:
        #get columns name of query
        re_result = re.search("SELECT (.*)\n",query)
        types = re_result.group(1).strip(" ").split("?")[1:]

        data = dict(zip(types, i))
        return data

    return dict()
