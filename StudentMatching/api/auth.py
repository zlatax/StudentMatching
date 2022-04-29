from flask import Blueprint, render_template, redirect, url_for, session, request
from flask import current_app as app
import bcrypt
import logging

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
        app.logger.warning("user logged in")
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        userEmail = request.form["inputEmail"]
        password = request.form["inputPassword"]
        
        user_found = verify_user(userEmail, password)

        if user_found[0]:
            app.logger.info("login success!")
            set_user_session(user_found[1])
            # session['user'] = user_found[1]
            return redirect(url_for("student.dashboard"))
        else:
            app.logger.error("user does not exist")
            message = "Email Address is not registered or password is not correct!"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")
    
@auth.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    if "user" in session:
        app.logger.warning("user logged in")
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":

        displayName = request.form.get("displayName")
        email = request.form.get("inputEmail")

        password1 = request.form.get("inputPassword1")
        password2 = request.form.get("inputPassword2")

        if email is None:
            app.logger.error("duplicate emailaddress")
            message = 'Please enter an email address'
            return render_template('signup.html', message=message)
        if password1 != password2:
            app.logger.error("password missmatch")
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed_password = bcrypt.hashpw(password2.encode(), salt)
            register = add_user(displayName, email, hashed_password)
            if register[0]:
                app.logger.info("user register success")
                set_user_session(register[1])
                # session["user"] = register[1]
                return redirect(url_for("student.dashboard"))
            else:
                app.logger.error("user register failure")
                message = register[1]
                return render_template("signup.html", message=message)
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    app.logger.info("user logout")
    session.clear()
    return render_template('home.html')