from flask import Blueprint, g
from ..errors import ValidationError, bad_request


api = Blueprint('api', __name__)


def get_catalog():
    return {}


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(str(e))


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')


@api.before_request
def before_request():
    pass


@api.after_request
def after_request(response):
    if hasattr(g, 'headers'):
        response.headers.extend(g.headers)
    return response

# do this last to avoid circular dependencies
from . import orders
