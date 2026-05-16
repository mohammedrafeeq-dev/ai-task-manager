from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from core.database import db
from features.organizations import org_bp
from features.organizations.forms import OrganizationForm
from features.organizations.models import Organization


@org_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.organization_id:
        return redirect(url_for("dashboard.index"))
    form = OrganizationForm()
    if form.validate_on_submit():
        if Organization.query.filter_by(slug=form.slug.data.strip()).first():
            form.slug.errors.append("Slug already taken.")
            return render_template("organizations/form.html", form=form)
        org = Organization(name=form.name.data.strip(), slug=form.slug.data.strip())
        db.session.add(org)
        db.session.flush()
        current_user.organization_id = org.id
        current_user.role = "admin"
        db.session.commit()
        flash("Organization created!", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("organizations/form.html", form=form)


@org_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if not current_user.organization_id:
        return redirect(url_for("organizations.create"))
    org = db.session.get(Organization, current_user.organization_id)
    if not org:
        flash("Organization not found.", "danger")
        return redirect(url_for("dashboard.index"))
    return render_template("organizations/settings.html", org=org)
