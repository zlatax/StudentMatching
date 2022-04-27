from flask import Blueprint, render_template, redirect, url_for, session, request

from .extensions import mongo, salt

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')