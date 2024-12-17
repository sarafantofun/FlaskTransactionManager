from flask_restx import Resource, fields, Namespace
from flask import request
from app.extensions import db
from app.models import User, Transaction


transaction_ns = Namespace('', description='Transaction API operations')

transaction_request_model = transaction_ns.model('TransactionRequest', {
    'user_id': fields.Integer(required=True, description="ID of the user associated with the transaction"),
    'amount': fields.Float(required=True, description="Transaction amount"),
})

transaction_response_model = transaction_ns.model('TransactionResponse', {
    'id': fields.Integer(readOnly=True, description="Transaction ID"),
    'amount': fields.Float(description="Transaction amount"),
    'commission': fields.Float(description="Automatically calculated commission"),
    'status': fields.String(description="Transaction status"),
    'created_at': fields.DateTime(description="Transaction creation time"),
    'user_id': fields.Integer(description="ID of the user associated with the transaction"),
})

cancel_transaction_request_model = transaction_ns.model('CancelTransactionRequest', {
    'transaction_id': fields.Integer(required=True, description="ID of the transaction to cancel"),
})

message_response_model = transaction_ns.model('MessageResponse', {
    'message': fields.String(description="Response message"),
})


@transaction_ns.route('/create_transaction')
class CreateTransaction(Resource):
    @transaction_ns.expect(transaction_request_model)
    @transaction_ns.response(201, 'Transaction successfully created', transaction_response_model)
    def post(self):
        """Создание транзакции с автоматическим расчетом комиссии"""
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        if not user_id or not amount:
            return {'message': 'User ID and Amount are required'}, 400
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        commission = amount * user.commission_rate
        transaction = Transaction(amount=amount, commission=commission, user_id=user_id)
        db.session.add(transaction)
        db.session.commit()
        return {
            'id': transaction.id,
            'amount': transaction.amount,
            'commission': transaction.commission,
            'status': transaction.status,
            'created_at': transaction.created_at.isoformat(),
            'user_id': transaction.user_id
        }, 201


@transaction_ns.route('/cancel_transaction')
class CancelTransaction(Resource):
    @transaction_ns.expect(cancel_transaction_request_model)
    @transaction_ns.response(200, 'Transaction successfully canceled', message_response_model)
    @transaction_ns.response(400, 'Invalid input', message_response_model)
    @transaction_ns.response(404, 'Transaction not found', message_response_model)
    def post(self):
        """Отмена транзакции по ID"""
        data = request.get_json()
        transaction_id = data.get('transaction_id')
        if not transaction_id:
            return {'message': 'Transaction ID is required'}, 400
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {'message': 'Transaction not found'}, 404
        if transaction.status != 'waiting':
            return {'message': 'Only transactions with status "waiting" can be canceled'}, 400
        transaction.status = 'canceled'
        db.session.commit()
        return {'message': f'Transaction {transaction_id} has been canceled'}, 200


@transaction_ns.route('/check_transaction')
class CheckTransaction(Resource):
    @transaction_ns.doc(params={'transaction_id': 'ID of the transaction to check'})
    @transaction_ns.response(200, 'Transaction details retrieved', transaction_response_model)
    @transaction_ns.response(400, 'Transaction ID is required', message_response_model)
    @transaction_ns.response(404, 'Transaction not found', message_response_model)
    def get(self):
        """Проверка статуса транзакции по ID"""
        transaction_id = request.args.get('transaction_id')
        if not transaction_id:
            return {'message': 'Transaction ID is required'}, 400
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {'message': 'Transaction not found'}, 404
        return {
            'id': transaction.id,
            'amount': transaction.amount,
            'commission': transaction.commission,
            'status': transaction.status,
            'created_at': transaction.created_at.isoformat()
        }, 200
