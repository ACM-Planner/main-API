"""
A module for managing errors.
"""


class InvalidUsage(Exception):
    """
    Generic class to handle requests' exceptions.

    Adapted from: http://flask.pocoo.org/docs/0.11/patterns/apierrors/
    ======= =====
    """

    DEFAULT_CODE = 400

    def __init__(self, message, payload=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        self.status_code = status_code or self.DEFAULT_CODE

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
