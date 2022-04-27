from flask_pymongo import PyMongo
import bcrypt

mongo = PyMongo()
salt = bcrypt.gensalt()