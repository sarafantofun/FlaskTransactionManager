from datetime import datetime, timedelta

from celery import shared_task

from app import create_app
from app.extensions import db
from app.models import Transaction

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@shared_task(ignore_result=False)
def expire_transactions():
    """
    Проверяет транзакции со статусом 'waiting' и меняет статус на 'expired',
    если прошло более 15 минут.
    """
    now = datetime.utcnow()
    expired_time = now - timedelta(minutes=15)

    transactions = Transaction.query.filter_by(status='waiting').filter(
        Transaction.created_at < expired_time
    ).all()

    for transaction in transactions:
        transaction.status = 'expired'
        db.session.commit()

    return f"{len(transactions)} транзакции(й) обновлены."
