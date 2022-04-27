from flask import Blueprint, render_template, redirect, url_for, session, request
import bcrypt

from .extensions import mongo, salt

auth = Blueprint('auth', __name__, url_prefix="/auth")



@auth.route("/login", methods=['post', 'get'])
def login():
    if request.method == "POST":
        userEmail = request.form["inputEmail"]
        entered_password = request.form["inputPassword"]
        entered_hashed = bcrypt.hashpw(entered_password.encode('utf-8'), salt)
        user_collection = mongo.db.users

        user = user_collection.find_one({'email':userEmail})
        if user:
            if user['password'] == entered_hashed:
                session['user'] = user
                return redirect(url_for("student.dashboard"))
    else:
        return render_template("login.html")
    
@auth.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    if "user" in session:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":

        displayName = request.form.get("displayName")
        email = request.form.get("inputEmail")

        password1 = request.form.get("inputPassword1")
        password2 = request.form.get("inputPassword2")

        user_collection = mongo.db.users

        email_found = user_collection.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), salt)
            user_input = {'name': displayName, 'email': email, 'password': hashed}

            user_collection.insert_one(user_input)
            
            user_data = user_collection.find_one({"email": email})
   
            return redirect(url_for("student.dashboard"))
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    session.clear()
    return render_template('home.html')