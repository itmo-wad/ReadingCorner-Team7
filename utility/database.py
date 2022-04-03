from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import uuid

# Only to be instantiated within this class
# To import and use this class in route files copy and paste this line: (or look at example in 'routes/login.py')
# from database import readingCornerDb [as customName]

# ReadingCorner database class
# New functions can be added at the bottom of the class
class readingCornerDatabase:
    def __init__(self):
        #self.client = MongoClient('localhost', 27017)
        self.client = MongoClient('mongodb+srv://axelportable:123test@cluster0.523ue.mongodb.net/test', 27017)
        self.db = self.client.readingcorner

        self.users = self.db.users
        self.links = self.db.links
        self.books = self.db.books

    # Returns all the users in the database
    def get_all_users(self):
        all_users = self.users.find()
        return all_users

    # Finds and returns a user based on a username
    def find_user(self, username):
        return self.users.find_one({"username": username})

    # Returns a user if one has the same userId
    def find_user_with_id(self, userId):
        return self.users.find_one({"id": userId})

    # Registers the user in the database by hashing his password and creating an unique id
    # TODO Modify this unique id to be able to link books to users via the links table
    def register_user(self, username, password):
        user = {
            "id": uuid.uuid4().hex,
            "username": username,
            "password": generate_password_hash(password)
        }
        while self.find_user_with_id(user["id"]):
            user["id"] = uuid.uuid4().hex
        self.users.insert_one(user)

    # Update the username of a user
    def update_user_username(self, user_id, new_username):
        query = {"id": user_id}
        newvalues = {"$set": {"username": new_username}}
        self.users.update_one(query, newvalues)

    # Update the password of a user
    def update_user_password(self, user_id, new_password):
        query = {"id": user_id}
        newvalues = {"$set": {"password": generate_password_hash(new_password)}}
        self.users.update_one(query, newvalues)


# ONLY instance of class within the app
readingCornerDb = readingCornerDatabase()