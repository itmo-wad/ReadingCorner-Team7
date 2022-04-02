from flask import Blueprint, redirect, url_for, render_template, request, flash
from utility.database import readingCornerDb as db
from utility.wraps import auto_login

register_page = Blueprint('register_page', __name__, template_folder='templates')

@register_page.route("/register", methods=["POST", "GET"])
@auto_login
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash ('You have to fill in all the fields.', 'error')
            return redirect(url_for('register_page.register'))
        elif db.find_user(username):
            flash('This username is already used.', 'error')
            return redirect(url_for('register_page.register'))
        else:
            db.register_user(username, password)
            return redirect('/')
    return render_template('register.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css","/static/css/register.css", "/static/css/main.css"])
