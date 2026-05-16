from datetime import date, datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from core.database import db
from features.tasks import tasks_bp
from features.tasks.forms import TaskForm
from features.tasks.models import Task, TaskComment
from features.tasks.pdf_service import export_task_report


def _parse_date(val):
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, date):
        return datetime.combine(val, datetime.min.time())
    try:
        return datetime.fromisoformat(str(val))
    except (ValueError, TypeError):
        return None


@tasks_bp.route("/")
@login_required
def list_tasks():
    tasks = Task.query.filter_by(organization_id=current_user.organization_id).order_by(Task.created_at.desc()).all()
    return render_template("tasks/list.html", tasks=tasks)


@tasks_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_task():
    if not current_user.organization_id:
        flash("Create or join an organization first.", "warning")
        return redirect(url_for("organizations.create"))
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=form.description.data.strip() if form.description.data else "",
            status=form.status.data,
            priority=form.priority.data,
            due_date=_parse_date(form.due_date.data),
            created_by_id=current_user.id,
            organization_id=current_user.organization_id,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, title="New Task")


@tasks_bp.route("/<task_id>")
@login_required
def view_task(task_id):
    task = db.session.get(Task, task_id)
    if not task or task.organization_id != current_user.organization_id:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/detail.html", task=task)


@tasks_bp.route("/<task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = db.session.get(Task, task_id)
    if not task or task.organization_id != current_user.organization_id:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = form.description.data.strip() if form.description.data else ""
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = _parse_date(form.due_date.data)
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("tasks.view_task", task_id=task.id))
    return render_template("tasks/form.html", form=form, title="Edit Task")


@tasks_bp.route("/<task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task or task.organization_id != current_user.organization_id:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/export/pdf")
@login_required
def export_pdf():
    if not current_user.organization_id:
        flash("No organization.", "warning")
        return redirect(url_for("organizations.create"))
    from features.organizations.models import Organization
    org = db.session.get(Organization, current_user.organization_id)
    org_name = org.name if org else "Unknown"
    tasks = Task.query.filter_by(organization_id=current_user.organization_id).order_by(Task.created_at.desc()).all()
    pdf_bytes = export_task_report(org_name, tasks, current_user.name)
    if not pdf_bytes:
        flash("Failed to generate PDF.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    from flask import Response
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=tasks_report_{datetime.now().strftime('%Y%m%d')}.pdf"},
    )
