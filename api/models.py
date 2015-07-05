from flask import url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column('id', db.String, primary_key=True)
    company_id = db.Column('company_id', db.String)
    status = db.Column('status', db.Integer, default=0)
    deliver_phone_number = db.Column('deliver_phone_number', db.String)
    loc_long = db.Column('loc_long', db.Float)
    loc_lat = db.Column('loc_lat', db.Float)

    def get_url(self):
        return url_for('api.get_order', order_id=self.order_id)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'loc': {
                'long': self.loc_long or "0.0",
                'lat': self.loc_lat or "0.0"
            },
            'status': self.status
        }


class Deliver(db.Model):
    __tablename__ = 'delivers'
    phone_number = db.Column('phone_number', db.String, primary_key=True)
    device_id = db.Column('device_id', db.String)