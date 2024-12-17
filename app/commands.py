from flask.cli import with_appcontext
from app.models import User, db


def register_commands(app):
    @app.cli.command("create-admin")
    @with_appcontext
    def create_admin():
        """Создаёт дефолтного администратора."""
        db.create_all()
        admin = User(
            balance=0.0,
            commission_rate=0.0,
            webhook_url="",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Администратор создан!")
