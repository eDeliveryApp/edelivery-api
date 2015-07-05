from flask import request, g
from ..models import db, Order
from ..decorators import json
from ..auth import login_required
from ..errors import bad_request
from . import api


@api.route('/orders', methods=['POST'])
@login_required
@json
def new_order():
    session_data = g.session_data
    data = request.get_json(force=True)
    if session_data['type'] != 'company' or not data.get('id', None):
        return bad_request('Not permission')
    order_ = Order()
    order_.company_id = session_data['company_id']
    order_.order_id = data['id']
    db.session.add(order_)
    db.session.commit()
    return {}, 201, {'Location': order_.get_url()}


@api.route('/orders/<order_id>', methods=['GET'])
@json
def get_order(order_id):
    return Order.query.filter(Order.order_id == order_id).first_or_404()


@api.route('/orders/<order_id>', methods=['PUT'])
@json
def edit_order(order_id):
    order_ = Order.query.filter(Order.order_id == order_id).first_or_404()
    data = request.get_json(force=True)
    if data.get('status', ''):
        order_.status = int(data['status'])
    if data.get('loc', {}):
        if not ('long' in data['loc'] and 'lat' in data['loc']):
            return bad_request('Invalid data["loc"]')
        else:
            order_.loc_long = data['loc']['long']
            order_.loc_lat = data['loc']['lat']
    if data.get('deliver_phone_number', ''):
        order_.deliver_phone_number = data['deliver_phone_number']
    db.session.add(order_)
    db.session.commit()
    return {"ok": True}