from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
api = Api()


def create_app():
    app = Flask(__name__)

    # Конфигурация приложения
    app.config.from_object('config.Config')

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Регистрация маршрутов
    with app.app_context():
        from app import views, api

    return app
