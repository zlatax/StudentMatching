from flask import Blueprint, render_template, session

from ..extensions import mongo

student = Blueprint('student', __name__,url_prefix='/student')

@student.route('/dashboard')
def dashboard():
    if 'user' in session:
        print(session['user'])
        return render_template('dashboard.html', user = session['user']) # matched_friends=matched_friends)
    else:
        return render_template('login.html')