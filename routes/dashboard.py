from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.database import readingCornerDatabase as db
from utility.wraps import require_login

dashboard_page = Blueprint('dashboard_page', __name__, template_folder='templates')

@dashboard_page.route("/dashboard")
@require_login
def dashboard():
    # TODO Get new releases from API
    new_releases = [{"cover":"/static/img/cover-TEST.jpg", "title":"50 shades of Grey", "author":"Yohann Goher", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"The way of nameless", "author":"Graham Douglass", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"}]

    my_books = [{"cover":"/static/img/cover-TEST.jpg", "title":"50 shades of Grey", "author":"Yohann Goher", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"The way of nameless", "author":"Graham Douglass", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"}]

    return render_template('louis-dashboard.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        "/static/css/main.css", "/static/css/dashboard.css"], releases=new_releases, books=my_books)