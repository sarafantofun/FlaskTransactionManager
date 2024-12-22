from datetime import datetime, timedelta

import requests
from celery import shared_task

from app import create_app
from app.extensions import db
from app.models import Transaction, User

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@shared_task(ignore_result=False)
def expire_transactions():
    """
    Проверяет транзакции со статусом 'waiting', меняет статус на 'expired'
    и отправляет вебхук с информацией о транзакции.
    """
    app_context = flask_app.app_context()
    with app_context:
        now = datetime.utcnow()
        expired_time = now - timedelta(minutes=15)
        transactions = Transaction.query.filter_by(status='waiting').filter(
            Transaction.created_at < expired_time
        ).all()
        for transaction in transactions:
            transaction.status = 'expired'
            db.session.commit()
            user = User.query.get(transaction.user_id)
            if user and user.webhook_url:
                payload = {
                    "transaction_id": transaction.id,
                    "status": transaction.status
                }
                try:
                    response = requests.post(user.webhook_url, json=payload)
                    response.raise_for_status()
                except requests.RequestException as e:
                    print(f"Webhook failed for Transaction {transaction.id}: {e}")
    return f"{len(transactions)} транзакции(й) обновлены."
