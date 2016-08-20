from flask import Blueprint
routes = Blueprint('routes', __name__)

from .root import *
from .courses import *
from .periods import *
from .triples import *
