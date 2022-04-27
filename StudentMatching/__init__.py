from dotenv import dotenv_values
from flask import Flask


from .extensions import mongo

from .main import main
from .student_services import student
from .auth import auth

def create_app(config_obj = "StudentMatching.settings"):
    app = Flask(__name__)
    app.secret_key="hell"

    app.config.from_object(config_obj)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    ## initialise db connection
    mongo.init_app(app)

    ## register blueprints
    app.register_blueprint(main) # /
    app.register_blueprint(auth) # /auth
    app.register_blueprint(student) # /student

    return app