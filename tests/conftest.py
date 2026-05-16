import os
import pytest
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from core.database import db as _db

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def app():
    app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, "templates"))
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = False

    _db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    Migrate(app, _db)

    @login_manager.user_loader
    def load_user(user_id):
        from features.auth.models import User
        return _db.session.get(User, user_id)

    from features.auth import auth_bp
    from features.organizations import org_bp
    from features.tasks import tasks_bp
    from features.ai import ai_bp
    from features.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(org_bp, url_prefix="/org")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(ai_bp, url_prefix="/ai")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.context_processor
    def inject_csrf():
        return {"csrf_token": lambda: ""}

    with app.app_context():
        _db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    """Register + create org. Returns the same client with auth cookies."""
    client.post("/auth/register", data={
        "name": "Test User", "email": "test@example.com",
        "password": "password123", "confirm": "password123",
    })
    client.post("/org/create", data={
        "name": "TestOrg", "slug": "testorg",
    })
    return client


@pytest.fixture
def task(auth):
    """Create a task and return its ID."""
    auth.post("/tasks/new", data={
        "title": "Test Task", "description": "Desc",
        "status": "todo", "priority": "high",
        "due_date": "2026-06-01",
    })
    from features.tasks.models import Task
    t = Task.query.first()
    return t.id if t else None
