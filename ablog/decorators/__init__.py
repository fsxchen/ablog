from functools import wraps

from flask import g, jsonify, request


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if (not hasattr(g, 'user')) or not g.user:
            return jsonify({"code": 40001}), 401
        return f(*args, **kwargs)
    return decorator


def pagination(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        g.paginate = {"per_page": int(request.args.get('limit', 2)), "page": int(request.args.get('page', 1))}
        return f(*args, **kwargs)
    return decorator
