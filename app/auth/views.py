from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import AuthForm, RegistrationForm
from ..models import User, Post, Role
from . import auth
from .. import db
from sqlalchemy import select


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = AuthForm()

    # user = User(id=1,username='admin',email='admin@admin.com',password_hash='1',role_id= 1)
    # user.password = 'admin'
    # db.session.add(user)
    # db.session.commit()
    if form.validate_on_submit():
        email = form.login.data
        user = User.query.filter_by(
            email=email
        ).first()  # select(User).where(User.username == email) #User.query.where(User.email=email).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role_id=2,
        )
        db.session.add(user)
        db.session.commit()
        # login_user(user, form.remember_me.data)
        return render_template("auth/account_created.html")
    return render_template("auth/registration.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))
