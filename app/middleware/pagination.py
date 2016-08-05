from functools import wraps
from flask import request

KEY = "page"
LIMIT = 100
INITIAL = 0


def paginate(limit=LIMIT, initial=INITIAL):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: catch parsing exceptions
            page = max(int(request.args.get(KEY, initial)), 0)
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
