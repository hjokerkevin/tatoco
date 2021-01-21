# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, current_app,redirect,url_for
from flask_login import login_required
from decorates import admin_required

user_blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@user_blueprint.route("/members")
@login_required
@admin_required
def members():
    """List members."""
    return render_template("users/members.html")

@user_blueprint.route("/login", methods=['POST'])
def login():
    if current_app.is_authencated:
        return redirect(url_for("index"))
    form = LoginForm()
    


