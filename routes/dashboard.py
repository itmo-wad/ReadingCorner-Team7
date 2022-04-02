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
    userid = request.cookies.get("userID")
    listbooks=list(mongo.db.isbn.find({"username":userid}))
    printbooks(listbooks)
    #print("listbooks=",listbooks)
    return render_template('dashboard.html', stylesheets=["/static/css/main.css"])

@dashboard_page.route('/test', methods=['POST']) 
def test(): 
    output = request.get_json()
    result = json.loads(output)
    userid = request.cookies.get("userID")
    print(userid)
    print(result)
    mongo.db.isbn.insert_one({"username":userid,"result":result})
    data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(result['bookIsbn']))
    infos = data.text
    infos_dict = json.loads(infos)
    infos2 = infos_dict['items'][0]
    #infos2_dict = json.loads(infos2)
    #print(infos2['volumeInfo']['title'])
    return result


# Function that takes the list of books of the current user, extract the ISBN from the database and do a request to the API with this ISBN. 
# As a result, we can extract the different parameters for the book in question.
def printbooks(listbooks):
    for i in range (len(listbooks)):
        result=listbooks[i]['result']['bookIsbn']
        data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(result))
        infos = data.text
        #print(infos)
        infos_dict = json.loads(infos)
        infos2 = infos_dict['items'][0]
        #infos2_dict = json.loads(infos2)
        print(infos2['volumeInfo']['title'])
        #print(infos2['volumeInfo'].get("imageLinks"))
        if infos2['volumeInfo'].get("imageLinks")==None:
            print("Default image")
        if infos2['volumeInfo'].get("imageLinks")!=None:
            print(infos2['volumeInfo'].get("imageLinks")['thumbnail'])  

