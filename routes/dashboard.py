<<<<<<< HEAD
from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
mongo = PyMongo(app)
=======
from flask import Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login
>>>>>>> 296fa7e94821ebcd403ceb0a7fd52caca3d545b2

dashboard_page = Blueprint('dashboard_page', __name__, template_folder='templates')

@dashboard_page.route("/dashboard")
@require_login
def dashboard():
<<<<<<< HEAD
    return render_template('dashboard.html', stylesheets=["/static/css/main.css"])

@dashboard_page.route('/test', methods=['POST']) 
def test(): 
    output = request.get_json()
    result = json.loads(output)
    print(result)
    mongo.db.isbn.insert_one({"result":result})
    return result
=======
    return render_template('dashboard.html', stylesheets=["/static/css/main.css"])
>>>>>>> 296fa7e94821ebcd403ceb0a7fd52caca3d545b2
