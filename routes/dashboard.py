from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login
from flask_pymongo import PyMongo
import json
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/readingcorner"
mongo = PyMongo(app)

dashboard_page = Blueprint('dashboard_page', __name__, template_folder='templates')

@dashboard_page.route("/dashboard")
@require_login
def dashboard():
    return render_template('dashboard.html', stylesheets=["/static/css/main.css"])

@dashboard_page.route('/test', methods=['POST']) 
def test(): 
    output = request.get_json()
    result = json.loads(output)
    print(result)
    mongo.db.isbn.insert_one({"result":result})
    data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(result['bookIsbn']))
    infos = data.text
    infos_dict = json.loads(infos)
    infos2 = infos_dict['items'][0]
    #infos2_dict = json.loads(infos2)
    print(infos2['volumeInfo']['title'])
    return result
