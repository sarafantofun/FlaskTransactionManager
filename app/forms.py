from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, ValidationError


class UserForm(FlaskForm):
    balance = FloatField('Баланс', validators=[DataRequired()])
    commission_rate = FloatField('Ставка комиссии', validators=[DataRequired()])
    webhook_url = StringField('Webhook URL', validators=[DataRequired(), URL()])
    role = SelectField('Роль', choices=[('user', 'User'), ('admin', 'Admin')])
    submit = SubmitField('Сохранить')


class TransactionForm(FlaskForm):
    amount = FloatField('Сумма', validators=[DataRequired()])
    commission = FloatField('Комиссия', validators=[DataRequired()])
    status = SelectField(
        'Статус',
        choices=[
            ('waiting', 'Ожидание'),
            ('confirmed', 'Подтверждена'),
            ('canceled', 'Отменена'),
            ('expired', 'Истекла')
        ]
    )
    submit = SubmitField('Сохранить')
    def validate_status(self, field):
        if field.data not in ['waiting', 'confirmed', 'canceled', 'expired']:
            raise ValidationError('Недопустимый статус транзакции.')
