from flask import Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login

dashboard_page = Blueprint('dashboard_page', __name__, template_folder='templates')

@dashboard_page.route("/dashboard")
@require_login
def dashboard():
    return render_template('dashboard.html', stylesheets=["/static/css/main.css"])