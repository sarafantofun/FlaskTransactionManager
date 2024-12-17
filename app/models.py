from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    commission_rate = db.Column(db.Float, default=0.0)
    webhook_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(10), default='user')  # admin или user
    usdt_wallet = db.Column(db.String(255), nullable=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, confirmed, canceled, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='transactions')
