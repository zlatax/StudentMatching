from flask import Blueprint, render_template

from .extensions import mongo

student = Blueprint('student', __name__,url_prefix='/student')

@student.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username="Thong", matched_friends=matched_friends)