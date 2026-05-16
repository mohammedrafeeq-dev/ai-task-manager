import os
from flask import Flask, jsonify
from config import Config, DevConfig, ProdConfig
from core.database import db
from core.extensions import init_extensions
from core.logging import setup_logging
from core.middleware import add_request_id


def create_app(config=None):
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", "development")
    if config is None:
        config = DevConfig() if env == "development" else ProdConfig()
    app.config.from_object(config)

    init_extensions(app)
    csrf = app.extensions.get("csrf")
    if csrf and not app.config.get("WTF_CSRF_ENABLED", True):
        csrf._csrf_disable = True
    setup_logging(app)

    app.before_request(add_request_id)

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
        return jsonify({"status": "ok"})

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("dashboard.index"))

    with app.app_context():
        from core.database import db
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
