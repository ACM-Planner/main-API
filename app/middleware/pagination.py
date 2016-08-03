from functools import wraps
from flask import request

LIMIT = 100


def paginate(key="page", limit=LIMIT, initial=0):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            page = int(request.args.get(key, initial))
            offset = page * LIMIT
            request.pagination = {
                "page": page,
                "offset": offset,
                "limit": limit,
            }
            return f(*args, **kwargs)
        return decorated_function
    return decorator
