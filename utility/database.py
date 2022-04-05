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
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.readingcorner
        self.users = self.db.users
        self.books = self.db.books

######################### USERS #########################

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

######################### BOOKS #########################

    # Return all books for an user
    def get_all_books_for_user(self, user_id):
        return self.books.find({"user_id": user_id})

    # Return a book if exists for a user by isbn
    def get_user_book_by_isbn(self, user_id, book_isbn):
        return self.books.find_one({"user_id": user_id, "isbn": book_isbn})

    # Return a book if exists for a user by isbn
    def get_current_reading_books(self, user_id):
        return self.books.find({"user_id": user_id, "status": "Reading"})

    # Change the status of the book, by default change to finished
    def update_book_status(self, user_id, book_isbn, new_status="Finished"):
        query = {"user_id": user_id, "isbn": int(book_isbn)}
        newvalues = {"$set": {"status": new_status}}
        print(query, newvalues)
        self.books.update_one(query, newvalues)

    # Update page number
    def update_page_number(self, user_id, book_isbn, new_page_number):
        query = {"user_id": user_id, "isbn": int(book_isbn)}
        newvalues = {"$set": {"progress": int(new_page_number)}}
        self.books.update_one(query, newvalues)

    # Add a book to a user
    def add_user_book(self, user_id, book_isbn, book_title,bookImg):
        new_book = {
#            "id": uuid.uuid4().hex,
            "user_id": user_id,
            "isbn": book_isbn,
            "title": book_title,
            "status": "Reading", # States : Reading / Finished
            "progress": 0,
            "bookImg": bookImg,
            
        }
        # Check if user already has book
        if not self.get_user_book_by_isbn(user_id, book_isbn):
            self.books.insert_one(new_book)

    # Delete book by isbn and user_id
    def delete_book_by_isbn_and_user(self, user_id, book_isbn):
        self.books.delete_one({'user_id': user_id, 'isbn': int(book_isbn)})


# ONLY instance of class within the app
readingCornerDb = readingCornerDatabase()
