from flask import Blueprint, render_template

from .extensions import mongo

student = Blueprint('student', __name__)

@student.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html', username="Thong", matched_friends=matched_friends)

@student.route("/logout", methods=["POST", "GET"])
    def logout():
        if "email" in session:
            session.pop("email", None)
            return render_template("signout.html")
        else:
            return render_template('index.html')