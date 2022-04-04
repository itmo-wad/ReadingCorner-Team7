from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.database import readingCornerDb as db
from utility.wraps import require_login
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/readingcorner"
mongo = PyMongo(app)

dashboard_page = Blueprint('dashboard_page', __name__, template_folder='templates')

@dashboard_page.route("/dashboard", methods = ["POST", "GET"])
@require_login
def dashboard():
    if request.method == "POST":
        isbn = request.form["isbn"]
        if "page" in request.form:
            new_page_number = request.form["page"]
            if not new_page_number:
                flash("Please enter a page number.", "error")
            else:
                if new_page_number.isnumeric():
                    db.update_page_number(request.cookies.get("userID"), isbn, new_page_number)
                    flash("Progress page of book updated.", "success")
                else:
                    flash("Page number must be a number.", "error")
            return redirect(url_for("dashboard_page.dashboard"))
        if "finished" in request.form:
            db.update_book_status(request.cookies.get('userID'), isbn)
            flash("Status of book updates to finished.", "success")

    current_books = db.get_current_reading_books(request.cookies.get("userID"))
    print("le current book",current_books)

    # TODO Get new releases from API
    new_releases = [{"cover":"/static/img/cover-TEST.jpg", "title":"50 shades of Grey", "author":"Yohann Goher", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"Comedy 101", "author":"Rowan Atkinson", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"},
                    {"cover":"/static/img/cover-TEST.jpg", "title":"The way of nameless", "author":"Graham Douglass", "link": "https://www.google.fr/books/edition/Blue_Highways/DTk3AQAAQBAJ?hl=en&gbpv=1"}]

    return render_template('dashboard.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        "/static/css/main.css", "/static/css/dashboard.css"], releases=new_releases, current_books=current_books, number_of_books = len(list(db.get_current_reading_books(request.cookies.get("userID")))))