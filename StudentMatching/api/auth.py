from flask import Blueprint, render_template, redirect, url_for, session, request
import bcrypt

from ..db import verify_user, add_user
from ..extensions import mongo, salt

USER_INFO = ['name', 'email']

auth = Blueprint('auth', __name__, url_prefix="/auth")

def set_user_session(usr):
    session['user'] = dict()
    for i in USER_INFO:
        session['user'][i] = usr[i]

@auth.route("/login", methods=['post', 'get'])
def login():
    if 'user' in session:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        userEmail = request.form["inputEmail"]
        password = request.form["inputPassword"]
        
        user_found = verify_user(userEmail, password)

        if user_found[0]:
            set_user_session(user_found[1])
            # session['user'] = user_found[1]
            return redirect(url_for("student.dashboard"))
        else:
            message = "Email Address is not registered or password is not correct!"
            return render_template("login.html", message=message)
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

        if email is None:
            message = 'Please enter an email address'
            return render_template('signup.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed_password = bcrypt.hashpw(password2.encode(), salt)
            register = add_user(displayName, email, hashed_password)
            if register[0]:
                set_user_session(register[1])
                # session["user"] = register[1]
                return redirect(url_for("student.dashboard"))
            else:
                message = register[1]
                return render_template("signup.html", message=message)
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    session.clear()
    return render_template('home.html')