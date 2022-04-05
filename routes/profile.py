from flask import Blueprint, redirect, url_for, render_template, request, flash
from werkzeug.security import check_password_hash
from utility.database import readingCornerDb as db
from utility.wraps import require_login

profile_page = Blueprint('profile_page', __name__, template_folder='templates')

@profile_page.route("/profile", methods=["POST", "GET"])
@require_login
def profile():
    user = db.find_user_with_id(request.cookies.get("userID"))
    if request.method == "POST":
        if "change-username" in request.form:
            new_username = request.form["username"]
            if not new_username:
                flash('You have not provided a username.', 'error')
            elif db.find_user(new_username):
                flash('Username already taken.', 'error')
            else:
                db.update_user_username(user["id"], new_username)
                flash('Successfully changed username.', 'success')
                return redirect('/profile')
        
        elif "change-password" in request.form:
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]
            if not old_password or not new_password or not confirm_password:
                flash("Please enter passwords.", 'error')
            elif not check_password_hash(user['password'], old_password):
                flash("Old password does not match.", 'error')
            elif new_password != confirm_password:
                flash("New passwords do not match.", 'error')
            else:
                db.update_user_password(user['id'], new_password)
                flash('Successfully updated password, please relogin.', 'success')
                return redirect('/disconnect')

    return render_template('profile.html', stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "/static/css/main.css", "/static/css/profile.css"], user=user)
