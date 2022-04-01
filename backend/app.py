from flask import Flask, render_template, request, flash, redirect, send_from_directory, session, jsonify,make_response
import os
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps
import datetime
import random

##### SESSION CONTROL #####

class User:
    def startSession(self, user):
        #del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['sessionid'] = str(random.randint(10**10, 10**20))
        return (user)

    def signup(self):
        user2 = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }
        user2['password'] = generate_password_hash(user2['password'])
        mongo.db.user.insert_one(user2)
        #return self.startSession(user2)
        #return jsonify(user2)
    
    def signout(self): #Ajouter un bouton
        session.clear()
        flash('You are now logged out')
        return redirect('/')

    

    def loggin (self):
        self.signout()
        username=request.form.get("username")
        password=request.form.get("password")
        user2 = {
            "username": username,
            "password": password,
        }
        return self.startSession(user2)


#Decorator that assure that we can not have access to certain pages if we are not logged in
def loggin_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        print(session["sessionid"],session['logged_in'])
        if session["sessionid"]==request.cookies.get("sessionid"):
            return f(*arg, **kwargs)
        else:
            flash ('You should first log in')
            return redirect('/login')
    return wrap

##### End SESSION CONTROL #####

##### MONGO CONFIGURATION #####
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
mongo = PyMongo(app)

##### END MONGO CONFIGURATION #####

##### ROUTES #####

# SIGN OUT 
@app.route('/user/signout')
def signout():
    return User().signout()

# HOMEPAGE
@app.route("/")
@loggin_required
def home_page():
    return render_template("dashboard.html")

#Register on the site
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.db.user.count_documents ({'username':username}) !=0:
            flash ('This name is already used')
            return redirect('/register')
        elif username == "" or password == "":
            flash ('You have to fill all the fields')
            return redirect('/register')
        else:
            return redirect('/login'), User().signup()


# Login
@app.route('/login', methods=["GET", "POST"])
def login ():
    if request.method == "GET":
        print(session['user']['username'])
        print(session['sessionid'])
        username=request.cookies.get("username")
        user = mongo.db.user.find_one({'username':username})
        if user and check_password_hash(user['password'], session['user']['password']) and (session['user']['username'] == request.cookies.get("username")) and (session['sessionid']==request.cookies.get("sessionid") ):
            return redirect('/')
        else:
            return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db.user.find_one({'username':username})
        if user and check_password_hash(user['password'], password) :
            timeExpire=datetime.datetime.utcnow() + datetime.timedelta(seconds=10)   #Set the expire time of the cookies. If the cookie is expire, when the user will come back to login, he will have to login again.
            User().loggin()
            resp=make_response(redirect('/'))
            resp.set_cookie('username',session['user']['username'],expires=timeExpire,httponly=True,secure=True)
            resp.set_cookie('sessionid',session['sessionid'],expires=timeExpire,httponly=True,secure=True)
            print(session['user']['username'])
            print(session['sessionid'])
            #flash('You are logged in, you can now write a post')
            #return render_template('list.html', username= username, passaword=password)
            return resp

        else:
            flash('Username or password is not correct')
            return redirect (request.url)


if __name__ == "__main__":
    app.secret_key = 'many random bytes'
    app.run(host='localhost', port=5002, debug=True)