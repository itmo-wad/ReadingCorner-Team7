from flask import Flask
from routes.login import login_page
from routes.register import register_page
from routes.dashboard import dashboard_page
from routes.profile import profile_page
from routes.bookshelf import bookshelf_page

# Creation of Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'
# Route blueprints
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(dashboard_page)
app.register_blueprint(profile_page)
app.register_blueprint(bookshelf_page)