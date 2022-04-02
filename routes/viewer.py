from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
from utility.wraps import require_login
from flask_pymongo import PyMongo
import json
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/readingcorner"
mongo = PyMongo(app)

viewer_page = Blueprint('viewer_page', __name__, template_folder='templates')

@viewer_page.route('/viewer' )
def lire():
    return render_template('viewer.html')
    #return render_template('viewer.html', isbn = result['bookIsbn'])