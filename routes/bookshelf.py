from flask import Blueprint, redirect, url_for, render_template, request, flash
from utility.database import readingCornerDb as db
from utility.wraps import require_login
import json
import requests

bookshelf_page = Blueprint('bookshelf_page', __name__, template_folder='templates')

@bookshelf_page.route("/bookshelf", methods=["POST", "GET"])
@require_login
def bookshelf():
    book_list=db.get_all_books_for_user(request.cookies.get("userID"))
    book_list=convert_books(list(book_list))
    print(book_list)
    return render_template('bookshelf.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "/static/css/main.css", "/static/css/bookshelf.css"], books=book_list)

# Function that takes the list of books of the current user, extract the ISBN from the database and do a request to the API with this ISBN. 
# As a result, we can extract the different parameters for the book in question.
def convert_books(listbooks):
    imageBooks=[]
    for i in range (len(listbooks)):
        result=listbooks[i]['isbn']
        data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(result))
        infos = data.text
        #print(infos)
        infos_dict = json.loads(infos)
        infos2 = infos_dict['items'][0]
        title = listbooks[i]['title']
        #print(infos2['volumeInfo']['title'])
        #print(infos2['volumeInfo'].get("imageLinks"))
        if infos2['volumeInfo'].get("imageLinks")==None:
            imageBooks.append(["No Image",result])
        if infos2['volumeInfo'].get("imageLinks")!=None:
            #print(infos2['volumeInfo'].get("imageLinks")['thumbnail'])  
            imageBooks.append([infos2['volumeInfo'].get("imageLinks")['thumbnail'],result])
    return imageBooks

@bookshelf_page.route('/add-book', methods=['POST'])
@require_login
def add_book():
    output = request.get_json()
    result = json.loads(output)
    db.add_user_book(request.cookies.get("userID"), result["bookIsbn"], result["title"])
    return result

@bookshelf_page.route('/remove-book', methods=['POST']) 
@require_login
def delete_book():
    db.delete_book_by_isbn_and_user(request.cookies.get("userID"), request.form.get('isbn'))
    return redirect('bookshelf')