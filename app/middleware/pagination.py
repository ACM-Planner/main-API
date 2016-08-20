from flask import request
from functools import wraps
from app.errors import InvalidUsage

KEY = "page"
LIMIT = 100
INITIAL = 0


def paginate(limit=LIMIT, initial=INITIAL):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                initial_ = request.args.get(KEY, initial)
                page = max(int(initial_), 0)
            except ValueError:
                ERROR_MESSAGE = ("{} is not a valid page format. "
                                 "Please, use an integer.")
                raise InvalidUsage(ERROR_MESSAGE.format(initial_),
                                   status_code=400)
            limited = max(min(int(request.args.get("limit", limit)), limit), 0)
            offset = page * limited
            request.pagination = {
                "page": page,
                "offset": offset,
                "limit": limited,
            }
            return f(*args, **kwargs)
        return decorated_function
    return decorator
