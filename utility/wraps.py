from flask import flash, redirect, request
from functools import wraps

# Wrap to require user to login before accessing this page
def require_login(f):
    @wraps(f)
    def wrap(*_, **__):
        if request.cookies.get("userID"):
            return f(*_, **__)
        else:
            flash('Access denied. Please login.', 'error')
            return redirect('/')
    return wrap

# Wrap to automatically relogin the user if his session is still valid
def auto_login(f):
    @wraps(f)
    def wrap(*_, **__):
        if request.cookies.get("userID"):
            flash("You were automatically reconnected.", 'success')
            return redirect('/dashboard')
        else:
            return f(*_, **__)
    return wrap