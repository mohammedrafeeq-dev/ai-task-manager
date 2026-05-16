from flask import render_template
from flask_login import current_user, login_required

from core.database import db
from features.dashboard import dashboard_bp
from features.tasks.models import Task


@dashboard_bp.route("/")
@login_required
def index():
    if not current_user.organization_id:
        return render_template("dashboard/index.html", stats=None)
    base = Task.query.filter_by(organization_id=current_user.organization_id)
    stats = {
        "total": base.count(),
        "todo": base.filter_by(status="todo").count(),
        "in_progress": base.filter_by(status="in_progress").count(),
        "done": base.filter_by(status="done").count(),
        "urgent": base.filter_by(priority="urgent").count(),
        "low": base.filter_by(priority="low").count(),
        "medium": base.filter_by(priority="medium").count(),
        "high": base.filter_by(priority="high").count(),
    }
    return render_template("dashboard/index.html", stats=stats)
