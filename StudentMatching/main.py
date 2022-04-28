from flask import Blueprint, render_template, redirect, url_for, session, request

from .extensions import mongo, salt

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/test')
def db_test():
    user_collection = mongo.db.users

    user = user_collection.find_one({'name':'test'})
    if user:
        return render("<h1>Success!</h1>")
    else:
        return render("<h1>Failed!</h1>")