import os
import rdflib
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from .errors import InvalidUsage
from .middleware.pagination import paginate

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
CORS(app)


@app.route("/", methods=["GET"])
def root():
    response = {"status": "on"}
    return jsonify(**response)


# GET /periods
@app.route("/periods", methods=["GET"])
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


# GET /courses
@app.route("/courses", methods=["GET"])
@paginate()
def courses():
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    # Period filtering
    year = request.args.get("year")
    period = request.args.get("period")
    if year and period:
        # Filter by period
        pass
    else:
        # By default do not take care about timeline
        pass

    # Search options
    initials = request.args.get("initials")
    name = request.args.get("name")
    nrc = request.args.get("nrc")
    category = request.args.get("category")
    teacher = request.args.get("teacher")
    campus = request.args.get("campus")
    school = request.args.get("school")

    # To satisfy schedule availability
    include_modules = request.args.get("include_modules")
    exclude_modules = request.args.get("exclude_modules", [])

    # To satisfy course requisites
    include_courses = request.args.get("include_courses")
    exclude_courses = request.args.get("exclude_courses", [])

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610
@app.route("/courses/<course_id>", methods=["GET"])
def course(course_id):
    data = dict()
    return jsonify(data=data)


# GET /courses/MAT1610/periods
@app.route("/courses/<course_id>/periods", methods=["GET"])
@paginate()
def course_periods(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/periods/2016/2/sections
@app.route("/courses/<course_id>/periods/<year>/<period>/sections", methods=["GET"])
@paginate()
def course_sections(course_id, year, period):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/periods/2016/2/sections/1
@app.route("/courses/<course_id>/periods/<year>/<period>/sections/<section_id>", methods=["GET"])
def course_section(course_id, year, period, section_id):
    data = dict()
    return jsonify(data=data)


# GET /courses/MAT1610/periods/2016/2/sections/1/teachers
@app.route("/courses/<course_id>/periods/<year>/<period>/sections/<section_id>/teachers", methods=["GET"])
@paginate()
def course_section_teachers(course_id, year, period, section_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/requisites
@app.route("/courses/<course_id>/requisites", methods=["GET"])
@paginate()
def course_requisites(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/corequisites
@app.route("/courses/<course_id>/corequisites", methods=["GET"])
@paginate()
def course_corequisites(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/opens
@app.route("/courses/<course_id>/opens", methods=["GET"])
@paginate()
def course_opens(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


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

    # data = []
    # for s, p, o in qres:
    #     data.append({"s": s, "p": p, "o": o})

    data = [{"s": s, "p": p, "o": o} for s, p, o in qres]

    # To JSON
    # json_string = qres.serialize(format="json")
    # print("JSON:", json_string)

    return jsonify(page=page, offset=offset, limit=limit, data=data)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
