import functools
from flask import request, current_app, g
from itsdangerous import URLSafeSerializer as Serializer
from errors import bad_request


def login_required(f):
    """This decorator adds an ETag header to the response."""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        s = Serializer(current_app.config['SECRET_KEY'])
        token = request.headers.get('eD-Token', '')
        if not token:
            return bad_request('Missing token')
        try:
            data = s.loads(token)
        except:
            return bad_request('Token incorrect')
        g.session_data = data
        return f(*args, **kwargs)
    return wrapped
