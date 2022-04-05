from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login

viewer_page = Blueprint('viewer_page', __name__, template_folder='templates')

@viewer_page.route('/viewer' )
@require_login
def lire():
    return render_template('viewer.html')