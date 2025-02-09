import os
from celery import Celery, Task
from flask import Flask

from app.extensions import db, migrate, api
from app.views import views_bp
from app.transaction_routes import transaction_ns


def celery_init_app(app):
    class FlaskTask(Task):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.flask_app = app

        def __call__(self, *args, **kwargs):
            with self.flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.Task = FlaskTask
    celery_app.config_from_object(app.config["CELERY"])
    if os.name == 'nt':
        celery_app.conf.worker_pool = 'solo'
    else:
        celery_app.conf.worker_pool = 'prefork'
    celery_app.conf.beat_schedule = {
        'expire-transactions-every-15-minutes':
        {
            "task": "app.tasks.expire_transactions",
            "schedule": 60.0
        }
    }
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
            task_ignore_result=False,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    from app.commands import register_commands
    register_commands(app)
    api.add_namespace(transaction_ns)
    app.register_blueprint(views_bp)
    return app
