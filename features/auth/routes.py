from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from core.database import db
from features.auth import auth_bp
from features.auth.forms import LoginForm, RegisterForm
from features.auth.models import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.strip()).first():
            form.email.errors.append("Email already registered.")
            return render_template("auth/register.html", form=form)
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("organizations.create"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
