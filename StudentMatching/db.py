import bson
import bcrypt

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson.json_util import loads, dumps

from .extensions import JSONEncoder


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

# Checks whether the user credentials exist and password matches the registered email.
def verify_user(email, password):
    found = db.users.find_one({'email':email})
    if found and bcrypt.checkpw(password.encode('UTF-8'), found['password'].encode('UTF-8')):
        return (True, found)
    else: 
        return (False, None)

def get_user(email):
    return db.users.find_one({'email':email})


# Attemps to add user to database, returns user dictionary if succeeds, 
# otherwise returns the error message.
def add_user(name, email, hashed_password):
    email_found = db.users.find_one({"email": email})
    if email_found:
        return (False, "This email already exists in database")
    else:
        new_user = {
            'name': name,
            'email': email,
            'password': hashed_password.decode()}
        result = db.users.insert_one(new_user)
        user = db.users.find_one({'email':email})
        return (True, user)
