from flask import Blueprint, g, current_app, request
from itsdangerous import URLSafeSerializer as Serializer
from .decorators import json
from .errors import bad_request
from .models import db, Deliver

token = Blueprint('token', __name__)


@token.route('/request-token', methods=['POST'])
@json
def request_token():
    data = request.get_json(force=True)
    if data.get('type', '') not in ('deliver', 'company'):
        return bad_request('')
    s = Serializer(current_app.config['SECRET_KEY'])
    if data['type'] == 'deliver':
        phone_number = data.get('phone_number', '')
        device_id = data.get('device_id', '')
        if not (phone_number and device_id):
            return bad_request('')
        deliver_ = Deliver.query.filter(Deliver.phone_number == phone_number).first()
        if not deliver_:
            deliver_ = Deliver()
            deliver_.phone_number = phone_number
            deliver_.device_id = device_id
        else:
            deliver_.device_id = device_id
        db.session.add(deliver_)
        db.session.commit()
        token_ = s.dumps({'type': data['type'], 'phone_number': phone_number}).decode('utf-8')
    else:
        company_id = data.get('company_id', '')
        if not company_id:
            return bad_request('')
        token_ = s.dumps({'type': data['type'], 'company_id': company_id}).decode('utf-8')
    return {'token': token_}
