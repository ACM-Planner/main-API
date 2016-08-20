from . import routes
from flask import request, jsonify
from app.app import * #FIX THIS IMPORT
from app.middleware.pagination import paginate

# GET /courses
@routes.route("/courses", methods=["GET"])
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
@routes.route("/courses/<course_id>", methods=["GET"])
def course(course_id):

    # Return name and faculty
    queryBasic = """
    SELECT ?name ?faculty
    WHERE {{
    ?x <http://cocke.ing.puc.cl/resource#initial> '{0}'.
    ?x <http://cocke.ing.puc.cl/resource#name_c> ?name.
    ?x <http://cocke.ing.puc.cl/resource#faculty> ?faculty.
    }}
    """.format(course_id)

    dataBasic = make_query(queryBasic)

    # Returns all requisites
    #  Total length of the requisite group and one of those members
    # Ex:
    #( ?total = 1 ) ( ?initial = "FIS1533" )
    #( ?total = 1 ) ( ?initial = "IEE2113" )
    #( ?total = 2 ) ( ?initial = "FIZ0221" )
    #( ?total = 2 ) ( ?initial = "IEE2113" )
    # is: [["FIS1533"], ["IEE2113"], ["FIZ0221", "IEE2113" ] ]


    queryRequires = """
    SELECT  ?initial ?total
    WHERE{{
       {{SELECT ?requires (COUNT(?b) as ?total )
        WHERE {{
        ?x <http://cocke.ing.puc.cl/resource#initial> '{0}'.
        ?x <http://cocke.ing.puc.cl/resource#requires> ?requires.
        ?requires ?a ?b.
        }}
        GROUP BY ?requires
        }}
    ?requires ?j ?k.
    ?k <http://cocke.ing.puc.cl/resource#initial> ?initial.
    }}
    ORDER BY ?requires
    """.format(course_id)

    dataRequires = []

    qres = graph.query(queryRequires)
    reading = 0
    list_requisites = []
    for i in qres:
        reading += 1
        list_requisites.append(i[0])
        if (reading >= int(str(i[1]))):
            dataRequires.append(list_requisites)
            reading = 0
            list_requisites = []


    queryEquivalent = """
    SELECT  ?initial
    WHERE{{
    ?x <http://cocke.ing.puc.cl/resource#initial> '{0}' .
    ?x <http://cocke.ing.puc.cl/resource#equivalent> ?k.
    ?k <http://cocke.ing.puc.cl/resource#initial> ?initial.
    }}
    """.format(course_id)

    dataEquivalent = make_query(queryEquivalent)

    return jsonify(data=dataBasic, requisites= dataRequires, equivalent= dataEquivalent)


# GET /courses/MAT1610/periods
@routes.route("/courses/<course_id>/periods", methods=["GET"])
@paginate()
def course_periods(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/periods/2016/2/sections
@routes.route("/courses/<course_id>/periods/<year>/<period>/sections", methods=["GET"])
@paginate()
def course_sections(course_id, year, period):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/periods/2016/2/sections/1
@routes.route("/courses/<course_id>/periods/<year>/<period>/sections/<section_id>", methods=["GET"])
def course_section(course_id, year, period, section_id):
    data = dict()
    return jsonify(data=data)


# GET /courses/MAT1610/periods/2016/2/sections/1/teachers
@routes.route("/courses/<course_id>/periods/<year>/<period>/sections/<section_id>/teachers", methods=["GET"])
@paginate()
def course_section_teachers(course_id, year, period, section_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/requisites
@routes.route("/courses/<course_id>/requisites", methods=["GET"])
@paginate()
def course_requisites(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/corequisites
@routes.route("/courses/<course_id>/corequisites", methods=["GET"])
@paginate()
def course_corequisites(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)


# GET /courses/MAT1610/opens
@routes.route("/courses/<course_id>/opens", methods=["GET"])
@paginate()
def course_opens(course_id):
    page = request.pagination["page"]
    offset = request.pagination["offset"]
    limit = request.pagination["limit"]

    data = []

    return jsonify(page=page, offset=offset, limit=limit, data=data)
