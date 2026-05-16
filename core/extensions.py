from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from core.database import db

login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from features.auth.models import User
        return db.session.get(User, user_id)
