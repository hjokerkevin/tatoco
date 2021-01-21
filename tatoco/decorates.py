from functools import wraps
from flask_login import current_app
from flask import flash, url_for, redirect, abort


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_app.confirmed:
            message = 'please confirm your account first.'
            flash(message, 'warning')
            return redirect(url_for("main.login"))
        return func(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    def decotator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_app.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decotator


def admin_required(func):
    return permission_required('ADMINISTER')(func)
    
