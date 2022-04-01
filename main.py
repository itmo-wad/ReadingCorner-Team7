from flask import Flask, render_template, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
import json


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/task2"
mongo = PyMongo(app)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route('/test', methods=['POST']) 
def test(): 
    output = request.get_json() 
    result = json.loads(output)
    print(result)
    print('haha')


if __name__ == "__main__":
    app.secret_key = 'many random bytes'
    app.run(host='localhost', port=5001, debug=True)

