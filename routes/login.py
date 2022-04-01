from flask import Blueprint, redirect, url_for, render_template, request, flash, make_response
from werkzeug.security import check_password_hash
from utility.database import readingCornerDb as db
from utility.wraps import auto_login, require_login

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route("/", methods = ['POST', 'GET'])
@auto_login
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username:
            flash('Please enter your username.', 'error')
        elif not password:
            flash('Please enter your password.', 'error')
        else:
            user = db.find_user(username)
            if user and check_password_hash(user['password'], password):
                flash('Logged in successfully.', "success")
                resp = make_response(redirect('/dashboard'))
                resp.set_cookie('userID', username)
                return resp
            else:
                flash("Wrong username or password.", "error")
                return redirect(url_for("login_page.login"))
    return render_template('login.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css","/static/css/login.css", "/static/css/main.css"])

@login_page.route("/disconnect")
@require_login
def disconnect():
    resp = make_response(redirect(url_for('login_page.login')))
    resp.delete_cookie('userID')
    flash("Successfully disconnected.", "success")
    return resp