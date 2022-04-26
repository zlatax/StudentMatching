import os

from dotenv import dotenv_values
from flask import Flask, render_template, url_for, request, session, redirect

from .extensions import mongo
from .student_services import student
from .main import main

def create_app(config = "setting."):
    app = Flask(__name__)
    app.secret_key="hello"

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    ## initialise db connection
    mongo.init_app(app)

    ## register blueprints
    app.register_blueprint(main)
    app.register_blueprint(student)

    return app