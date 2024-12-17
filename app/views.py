from datetime import datetime

from flask import render_template, redirect, url_for, request, flash, Blueprint
from app import db
from app.forms import UserForm, TransactionForm
from app.models import User, Transaction


views_bp = Blueprint('views', __name__, url_prefix='/admin')


@views_bp.route('/dashboard')
def dashboard():
    users_count = User.query.count()
    transactions_count = Transaction.query.count()
    today = datetime.utcnow().date()
    daily_transactions_sum = db.session.query(
        db.func.sum(Transaction.amount)
    ).filter(
        db.func.date(Transaction.created_at) == today
    ).scalar() or 0
    latest_transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).limit(10).all()
    return render_template(
        'dashboard.html',
        users_count=users_count,
        transactions_count=transactions_count,
        daily_transactions_sum=daily_transactions_sum,
        latest_transactions=latest_transactions
    )


@views_bp.route('/users', methods=['GET', 'POST'])
def users():
    form = UserForm()
    form_action = url_for('views.users')
    form_title = "Создать пользователя"
    edit_user_id = request.args.get('edit_user_id', type=int)
    if edit_user_id:
        user = User.query.get_or_404(edit_user_id)
        form = UserForm(obj=user)
        form_action = url_for('views.users', edit_user_id=edit_user_id)
        form_title = f"Редактировать пользователя #{user.id}"
    if form.validate_on_submit():
        if edit_user_id:
            user.balance = form.balance.data
            user.commission_rate = form.commission_rate.data
            user.webhook_url = form.webhook_url.data
            user.role = form.role.data
            flash(f'Пользователь #{user.id} успешно обновлён!', 'success')
        else:
            user = User(
                balance=form.balance.data,
                commission_rate=form.commission_rate.data,
                webhook_url=form.webhook_url.data,
                role=form.role.data
            )
            db.session.add(user)
            flash('Пользователь успешно создан!', 'success')
        db.session.commit()
        return redirect(url_for('views.users'))
    if request.method == 'POST' and 'delete_user_id' in request.form:
        user_id = request.form['delete_user_id']
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь #{user_id} успешно удалён!', 'success')
        return redirect(url_for('views.users'))
    all_users = User.query.all()
    return render_template('users.html', users=all_users, form=form, form_action=form_action, form_title=form_title)


@views_bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
    edit_transaction_id = request.args.get('edit_transaction_id', type=int)
    transaction = Transaction.query.get(edit_transaction_id) if edit_transaction_id else None
    form = TransactionForm(obj=transaction)
    form_title = f"Редактировать транзакцию #{transaction.id}" if transaction else "Выберите транзакцию для редактирования"
    if form.validate_on_submit():
        if transaction:
            transaction.amount = form.amount.data
            transaction.commission = form.commission.data
            transaction.status = form.status.data
            db.session.commit()
            flash(f'Транзакция #{transaction.id} успешно обновлена!', 'success')
            return redirect(url_for('views.transactions'))
    all_transactions = Transaction.query.all()
    return render_template(
        'transactions.html',
        transactions=all_transactions,
        form=form,
        form_title=form_title,
        edit_transaction_id=edit_transaction_id
    )
