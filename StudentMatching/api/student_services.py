from flask import Blueprint, render_template, session
from flask import current_app as app

from ..extensions import mongo

from ..sample_users import users

student = Blueprint('student', __name__,url_prefix='/student')

@student.route('/dashboard')
def dashboard():
    if 'user' in session:
        app.logger.info("welcome back")
        return render_template('dashboard.html', user = session['user'], matched_usrs=users)
    else:
        app.logger.warning("not logged-in")
        return render_template('login.html')